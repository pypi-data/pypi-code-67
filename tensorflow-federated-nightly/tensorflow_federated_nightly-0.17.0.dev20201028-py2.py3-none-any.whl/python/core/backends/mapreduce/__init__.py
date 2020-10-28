# Copyright 2019, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Libraries for interacting with MapReduce-like backends.

This package contains libraries for using TFF in backend systems that offer
MapReduce-like capabilities, i.e., systems that can perform parallel processing
on a set of clients, and then aggregate the results of such processing on the
server. Systems of this type do not support the full expressiveness of TFF, but
they are common enough in practice to warrant a dedicated set of libraries, and
many examples of TFF computations, including those constructed by
`tff.learning`, can be compiled by TFF into a form that can be deployed on such
systems.

This package defines a data structure `CanonicalForm`, parameterized by
TensorFlow functions, which expresses the logic of a single MapReduce-style
round (plus initialization) and serves as a target for TFF's compiler pipeline.

`CanonicalForm` serves as the conceptual core of this package, and represents
a manner of specifying a round of federated computation quite distinct from
TFF's usual `computation.proto`. However, as `CanonicalForm` can express only a
strict subset of the logic expressible via `computation.proto`, we discuss the
mapping between the two here.

Instead of `computation.proto` directly, we standardize on
`tff.templates.IterativeProcess` as the basis for targeting the canonical
mapreduce representation, as this type of processing is most common in federated
learning scenarios, where different rounds typically involve different subsets
of a potentially very large number of participating clients. The iterative
aspect of the computation allows for it to not only model processes that evolve
over time, but also ones that might involve a very large client population in
which not all participants (clients, data shards, etc.) may be present at the
same time, and the iterative approach may instead be dictated by data
availability or scalability considerations. Related to the above, the fact that
in practical scenarios the set of clients involved in a federated computation
will (often) vary from round to round, the server state is necessary to connect
subsequent rounds into a single contiguous logical sequence.

Conceptually, `next`, the iterator part of an iterative process, is modeled
in the same way as any stateful computation in TFF. I.e., one that takes the
server state as the first component of the input, and returns updated server
state as the first component of the output. If there is no need for server
state, the input/output state should be modeled as an empty tuple.

In addition to updating state, `next` additionally takes client-side data as
input, and can produce results on server side in addition to state intended to
be passed to the next round. As is the case for the server state, if this
is undesired it should be modeled as an empty tuple.

The type signature of `next`, in the concise TFF type notation (as defined in
TFF's `computation.proto`), is as follows:

```python
(<S@SERVER,{D}@CLIENTS> -> <S@SERVER,X@SERVER>)
```

The above type signature involves the following abstract types:

* `S` is the type of the state that is passed at the server between rounds of
  processing. For example, in the context of federated training, the server
  state would typically include the weights of the model being trained. The
  weights would be updated in each round as the model is trained on more and
  more of the clients' data, and hence the server state would evolve as well.

  Note: This is also the type of the output of the `initialize` that produces
  the server state to feed into the first round.

* `D` represents the type of per-client units of data that serve as the input
  to the computation. Often, this would be a sequence type, i.e., a dataset
  in TensorFlow's parlance, although strictly speaking this does not have to
  always be the case.

* `X` represents the type of server-side outputs generated by the server after
  each round.

One can think of the process based on this representation as being equivalent
to the following pseudocode loop:

```python
client_data = ...
server_state = initialize()
while True:
  server_state, server_outputs = next(server_state, client_data)
```

The logic of `next` in `CanonicalForm` is factored into seven
variable components `prepare`, `work`, `zero`, `accumulate`, `merge`,
`report`, and `update` (in addition to `initialize` that produces the server
state component for the initial round and `bitwidth` that specifies runtime
parameters for `federated_secure_sum`). The pseudocode below uses common
syntactic shortcuts (such as implicit zipping) for brevity.

For a concise representation of the logic embedded in the discussion below,
specifying the manner in which an instance `cf` of `CanonicalForm` maps to
a single federated round, see the definitions of `init_computation` and
`next_computation` in
`form_utils.get_iterative_process_for_canonical_form`.

```python
@tff.federated_computation
def next(server_state, client_data):

  # The server prepares an input to be broadcast to all clients that controls
  # what will happen in this round.

  client_input = (
    tff.federated_broadcast(tff.federated_map(prepare, server_state)))

  # The clients all independently do local work and produce updates, plus the
  # optional client-side outputs.

  client_updates = tff.federated_map(work, [client_data, client_input])

  # `client_updates` is a two-tuple, whose first index should be aggregated
  # with TFF's `federated_aggregate` and whose second index should be passed
  # to TFF's `federated_secure_sum`.  The  updates are aggregated across the
  # system into a single global update at the server.

  simple_agg = (
    tff.federated_aggregate(client_updates[0], zero(), accumulate, merge,
        report))
  secure_agg = tff.secure_sum(client_updates[1], bitwidth())

  global_update = [simple_agg, secure_agg]

  # Finally, the server produces a new state as well as server-side output to
  # emit from this round.

  new_server_state, server_output = (
    tff.federated_map(update, [server_state, global_update]))

  # The updated server state, server- and client-side outputs are returned as
  # results of this round.

  return new_server_state, server_output
```

The above characterization of `next` forms the relationship between
`CanonicalForm` and `tff.templates.IterativeProcess`. It depends on the seven
pieces of pure TensorFlow logic defined as follows. Please also consult the
documentation for related federated operators for more detail (particularly
the `tff.federated_aggregate()`, as several of the components below correspond
directly to the parameters of that operator).

* `prepare` represents the preparatory steps taken by the server to generate
  inputs that will be broadcast to the clients and that, together with the
  client data, will drive the client-side work in this round. It takes the
  initial state of the server, and produces the input for use by the clients.
  Its type signature is `(S -> C)`.

* `work` represents the totality of client-side processing, again all as a
  single section of TensorFlow code. It takes a tuple of client data and
  client input that was broadcasted by the server, and returns a two-tuple
  containing the client update to be aggregated (across all the clients). The
  first index of this two-tuple will be passed to an aggregation parameterized
  by the blocks of TensorFlow below (`zero`, `accumulate`, `merge`, and
  `report`), and the second index will be passed to `federated_secure_sum`.
  Its type signature is `(<D,C> -> <U,V>)`.

* `bitwidth` is the TensorFlow computation that produces an integer specifying
  the bitwidth for inputs to secure sum. `bitwidth` will be used by the system
  to compute appropriate parameters for the secure sum protocol. Exactly how
  this computation is performed is left to the runtime implementation of
  `federated_secure_sum`.

* `zero` is the TensorFlow computation that produces the initial state of
  accumulators that are used to combine updates collected from subsets of the
  client population. In some systems, all accumulation may happen at the
  server, but for scalability reasons, it is often desirable to structure
  aggregation in multiple tiers. Its type signature is `A`, or when
  represented as a `tff.Computation` in Python, `( -> A)`.

* `accumulate` is the TensorFlow computation that updates the state of an
  update accumulator (initialized with `zero` above) with a single client's
  update. Its type signature is `(<A,U> -> A)`. Typically, a single acumulator
  would be used to combine the updates from multiple clients, but this does
  not have to be the case (it's up to the target deployment platform to choose
  how to use this logic in a particular deployment scenario).

* `merge` is the TensorFlow computation that merges two accumulators holding
  the results of aggregation over two disjoint subsets of clients. Its type
  signature is `(<A,A> -> A)`.

* `report` is the TensorFlow computation that transforms the state of the
  top-most accumulator (after accumulating updates from all clients and
  merging all the resulting accumulators into a single one at the top level
  of the system hierarchy) into the final result of aggregation. Its type
  signature is `(A -> R)`.

* `update` is the TensorFlow computation that applies the aggregate of all
  clients' updates (the output of `report`), also referred to above as the
  global update, to the server state, to produce a new server state to feed
  into the next round, and that additionally outputs a server-side output,
  to be reported externally as one of the results of this round. In federated
  learning scenarios, the server-side outputs might include things like loss
  and accuracy metrics, and the server state to be carried over, as noted
  above, may include the model weights to be trained further in a subsequent
  round. The type signature of this computation is `(<S,R> -> <S,X>)`.

The above TensorFlow computations' type signatures involves the following
abstract types in addition to those defined earlier:

* `C` is the type of the inputs for the clients, to be supplied by the server
  at the beginning of each round (or an empty tuple if not needed).

* `U` is the type of the per-client update to be produced in each round and
  fed into the cross-client federated aggregation protocol.

* `V` is the type of the per-client update to be produced in each round and
  fed into the cross-client secure aggregation protocol.

* `A` is the type of the accumulators used to combine updates from subsets of
  clients.

* `R` is the type of the final result of aggregating all client updates, the
  global update to be incorporated into the server state at the end of the
  round (and to produce the server-side output).
"""

# TODO(b/138261370): Cover this in the general set of guidelines for deployment.

from tensorflow_federated.python.core.backends.mapreduce.form_utils import get_canonical_form_for_iterative_process
from tensorflow_federated.python.core.backends.mapreduce.form_utils import get_iterative_process_for_canonical_form
from tensorflow_federated.python.core.backends.mapreduce.forms import BroadcastForm
from tensorflow_federated.python.core.backends.mapreduce.forms import CanonicalForm

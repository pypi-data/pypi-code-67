"""

Custom PyTorch modules. Each class must implement torch.nn.Module, and therefore must have an __init__ method and a forward method.

"""
from __future__ import annotations
from typing import Iterable, Optional, Tuple

import collections
import networkx as nx
import torch

__all__ = [
    "Concatenate",
    "ElmanRNN",
    "FC",
    "FCRNN",
    "GraphNetwork",
    "Module",
    "Reshape",
    "WAVE",
]


class Module(torch.nn.Module):
    def __init__(
        self,
        module: torch.nn.Module,
        activation: Optional[Callable[..., torch.Tensor]] = None,
    ) -> None:
        super().__init__()
        self.module = module
        self.activation = activation or (lambda x: x)

    def forward(self, *args: torch.Tensor, **kwargs: torch.Tensor) -> torch.Tensor:
        return self.activation(self.module(*args, **kwargs))


class Concatenate(torch.nn.Module):
    def __init__(self, dim: Optional[int] = 0) -> None:
        super().__init__()
        self.dim = dim

    def forward(self, *tensors: torch.Tensor) -> torch.Tensor:
        return torch.cat(tensors, dim=self.dim)


class ElmanRNN(torch.nn.Module):
    def __init__(
        self,
        input_size,
        hidden_size,
        num_layers=None,
        nonlinearity=None,
        bias=None,
        batch_first=None,
        dropout=None,
        bidirectional=None,
        h0=None,
    ):
        super().__init__()

        self.hidden_size = hidden_size

        kwargs = {}
        if num_layers:
            kwargs["num_layers"] = num_layers
        if nonlinearity:
            kwargs["nonlinearity"] = nonlinearity
        if bias:
            kwargs["bias"] = bias
        if batch_first:
            kwargs["batch_first"] = batch_first
        if dropout:
            kwargs["dropout"] = dropout
        if bidirectional:
            kwargs["bidirectional"] = bidirectional

        self.h0 = h0
        self.rnn = torch.nn.RNN(
            input_size=input_size, hidden_size=hidden_size, **kwargs
        )

    def forward(self, x):
        if self.h0:
            output, hidden = self.rnn.forward(input=x, h0=self.h0)
        else:
            output, hidden = self.rnn.forward(input=x)
        return output


class FC(torch.nn.Module):
    def __init__(self, in_features, out_features, *hidden_features):
        super().__init__()
        sizes = tuple((in_features, *hidden_features, out_features))
        layers = (
            torch.nn.Linear(in_features=n_in, out_features=n_out)
            for n_in, n_out in zip(sizes, sizes[1:])
        )
        self.seq = torch.nn.Sequential(*layers)

    def forward(self, x):
        return self.seq(x)


class FCRNN(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.hidden_size = hidden_size
        self.hidden = self._init_hidden()

        self.i2h = torch.nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = torch.nn.Linear(input_size + hidden_size, output_size)

    def forward(self, x):
        self.hidden = self._init_hidden()

        for i in x.transpose(0, 1):
            combined = torch.cat((i, self.hidden), 1)
            self.hidden = self.i2h(combined)
            output = self.i2o(combined)

        return output

    def _init_hidden(self):
        return torch.zeros(1, self.hidden_size)


# class GraphNetwork(torch.nn.Module):
#     def __init__(self, node_dim: int, edge_dim: int, global_dim: int, num_layers: Optional[int] = 1) -> None:
#         super().__init__()
#         self.node_dim = node_dim
#         self.edge_dim = edge_dim
#         self.global_dim = global_dim
#         self.num_layers = num_layers

#     def forward(self, nodes: torch.Tensor, edges: torch.Tensor, edge_index: torch.Tensor, batch: Optional[torch.Tensor] = None, u: Optional[torch.Tensor] = None) -> torch.Tensor:
#         if batch is None:
#             N_v, *_ = nodes.shape
#             batch = torch.zeros((N_v,),dtype=torch.long)
#         for _ in range(self.num_layers):
#             edges = self.update_edges(edges,edge_index,nodes,batch,u).reshape(edges.shape)

#             aggregated_edges = self.aggregate_edges_local(nodes,edges,edge_index,batch,u)
#             nodes = self.update_nodes(nodes,aggregated_edges,edge_index,batch,u).reshape(nodes.shape)

#             aggregated_node = self.aggregate_nodes(nodes,edge_index,batch)
#             aggregated_edge = self.aggregate_edges(edges,edge_index,batch)
#             u = self.update_global(aggregated_node,aggregated_edge,batch,u).reshape(u.shape)

#         return nodes,edges,edge_index,u

#     def update_edges(self, edges: torch.Tensor, edge_index: torch.Tensor, nodes: torch.Tensor, batch: torch.Tensor, u: torch.Tensor) -> torch.Tensor:
#         # output.shape = (N_e,edge_dim)
#         raise NotImplementedError

#     def update_nodes(self, nodes: torch.Tensor, aggregated_edges: torch.Tensor, edge_index: torch.Tensor, batch: torch.Tensor, u: torch.Tensor) -> torch.Tensor:
#         # output.shape = (N_v,node_dim)
#         raise NotImplementedError

#     def update_global(self, aggregated_nodes: torch.Tensor, aggregated_edges: torch.Tensor, batch: torch.Tensor, u: torch.Tensor) -> torch.Tensor:
#         # output.shape = u.shape
#         raise NotImplementedError

#     def aggregate_edges_local(self, nodes: torch.Tensor, edges: torch.Tensor, edge_index: torch.Tensor, batch: torch.Tensor, u: torch.Tensor) -> torch.Tensor:
#         # output.shape = (N_v,edge_dim)
#         raise NotImplementedError

#     def v_to_u(self, nodes: torch.Tensor, edge_index: torch.Tensor, batch: torch.Tensor) -> torch.Tensor:
#         # output.shape = (1,node_dim)
#         raise NotImplementedError

#     def aggregate_edges(self, edges: torch.Tensor, edge_index: torch.Tensor, batch: torch.Tensor) -> torch.Tensor:
#         # output.shape = (1,global_dim)
#         raise NotImplementedError


class GraphNetwork(torch.nn.Module):
    def __init__(
        self,
        edge_model: Optional[torch.nn.Module] = None,
        node_model: Optional[torch.nn.Module] = None,
        global_model: Optional[torch.nn.Module] = None,
        num_layers: Optional[int] = 1,
    ) -> None:
        super().__init__()
        self.edge_model = edge_model
        self.node_model = node_model
        self.global_model = global_model
        self.num_layers = num_layers

    def forward(
        self,
        nodes: torch.Tensor,
        edge_index: torch.Tensor,
        edges: Optional[torch.Tensor] = None,
        u: Optional[torch.Tensor] = None,
        batch: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        if batch is None:
            N_v, *_ = nodes.shape
            batch = torch.zeros((N_v,), dtype=torch.long)

        for _ in range(self.num_layers):
            if self.edge_model is not None:
                edges = self.edge_model(nodes, edge_index, edges, u, batch).reshape(
                    edges.shape
                )

            if self.node_model is not None:
                nodes = self.node_model(nodes, edge_index, edges, u, batch).reshape(
                    nodes.shape
                )

            if self.global_model is not None:
                u = self.global_model(nodes, edge_index, edges, u, batch).reshape(
                    u.shape
                )

        return nodes, edge_index, edges, u, batch

    # def forward(self, nodes: torch.Tensor, edges: torch.Tensor, edge_index: torch.Tensor, batch: Optional[torch.Tensor] = None, u: Optional[torch.Tensor] = None) -> torch.Tensor:
    #     if batch is None:
    #         N_v, *_ = nodes.shape
    #         batch = torch.zeros((N_v,),dtype=torch.long)

    #     for _ in range(self.num_layers):
    #         edges = self.update_edges(edges,edge_index,nodes,batch,u).reshape(edges.shape)

    #         aggregated_edges = self.aggregate_edges_local(nodes,edges,edge_index,batch,u)
    #         nodes = self.update_nodes(nodes,aggregated_edges,edge_index,batch,u).reshape(nodes.shape)

    #         aggregated_node = self.aggregate_nodes(nodes,edge_index,batch)
    #         aggregated_edge = self.aggregate_edges(edges,edge_index,batch)
    #         u = self.update_global(aggregated_node,aggregated_edge,batch,u).reshape(u.shape)

    #     return nodes,edges,edge_index,u


class Reshape(torch.nn.Module):
    def __init__(self, out_shape: Iterable[int]) -> None:
        super().__init__()
        self.shape = tuple(out_shape)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x.view(self.shape)


class WAVE(torch.nn.Module):
    def __init__(self, atom_feature_size: int, num_passes: int) -> None:
        super().__init__()

        self.d = atom_feature_size
        self.num_passes = num_passes

        self.T_to_A = torch.nn.Linear(in_features=2 * self.d, out_features=self.d)
        self.C_to_A = torch.nn.Linear(in_features=2 * self.d, out_features=self.d)
        self.T_to_B = torch.nn.Linear(in_features=2 * self.d, out_features=self.d)
        self.C_to_B = torch.nn.Linear(in_features=2 * self.d, out_features=self.d)
        self.softmax_mix = Module(Concatenate(dim=1), torch.nn.Softmax(dim=1))
        self.softsign_mix = Module(Concatenate(dim=1), torch.nn.Softsign())
        self.W = torch.randn(size=(self.d, 1))
        self.W_u = Module(
            torch.nn.Linear(in_features=2 * self.d, out_features=self.d),
            torch.nn.Sigmoid(),
        )
        self.W_o = Module(
            torch.nn.Linear(in_features=2 * self.d, out_features=self.d),
            torch.nn.ReLU(),
        )

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        # FIXME: is this really the only way to handle batches of disjoint graphs?
        out = []
        for _x, _edge_index in zip(x, edge_index):
            traversal_order = self._traverse_graph(_x, _edge_index)

            lengths = tuple(len(l) for l in traversal_order)
            perm = torch.eye(sum(lengths))[[a for b in traversal_order for a in b]]

            _x = torch.matmul(perm, _x).t()

            for _ in range(self.num_passes):
                self._propagate(_x, lengths)
                self._propagate(_x, lengths[::-1])

            out.append(_x.t())

        return torch.stack(out, dim=0)

    def _traverse_graph(self, x: torch.Tensor, edge_index: torch.Tensor) -> Tuple[int]:
        # FIXME: if a graph has nodes with no edges, this leads to an error inside of forward
        # because edge_index does not reference them and so they are not included in the traversal order
        # but they are still included in x
        g = nx.Graph(list(edge_index.t().numpy()))

        root, *_ = nx.center(g)

        digraph = nx.bfs_tree(g, root)

        order = [[root]]
        while sum(len(a) for a in order) < len(g):
            # FIXME: not sure what this ordered dict stuff actually does if anything...
            succs = list(
                collections.OrderedDict.fromkeys(
                    [r for s in order[-1] for r in list(digraph.successors(s))]
                ).keys()
            )
            order.append(succs)

        return order

    def _propagate(self, x: torch.Tensor, lengths: Iterable[int]) -> None:
        offset = 0
        # NOTE/FIXME: using update avoids a RuntimeError due to editing x in place
        update = torch.zeros_like(x)
        for t, c in zip(lengths, lengths[1:]):
            i = offset + t
            j = i + c

            T = x[:, offset:i]
            C = x[:, i:j]
            N = x[:, offset:j]

            for k in range(c):
                s = C.narrow(dim=1, start=k, length=1)

                m = self._mix_gate(state=s, tree=T, cross=C, neighbors=N)

                u = self.W_u(torch.cat(tensors=[m, s], dim=0).t()).t()
                o = self.W_o(torch.cat(tensors=[m, s], dim=0).t()).t()

                # NOTE: subtract s to replace the column in x with the update
                update[:, i:j][:, k : k + 1] = u * o + (1 - u) * m - s

            x = x + update
            offset += t

    def _mix_gate(
        self,
        state: torch.Tensor,
        tree: torch.Tensor,
        cross: torch.Tensor,
        neighbors: torch.Tensor,
    ) -> torch.Tensor:
        input_T = torch.cat([tree, state.expand_as(tree)], dim=0).t()
        input_C = torch.cat([cross, state.expand_as(cross)], dim=0).t()

        A = self.softmax_mix(
            self.T_to_A(input_T).t(), self.C_to_A(input_C).t()
        ) * self.W.expand_as(neighbors)

        B = self.softsign_mix(self.T_to_B(input_T).t(), self.C_to_B(input_C).t())

        return torch.sum((A + B) * neighbors, dim=1).unsqueeze(1)

# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

import cirq
import cirq.testing as ct
import cirq.contrib.acquaintance as cca

def test_remove_redundant_acquaintance_opportunities():
    device = cca.UnconstrainedAcquaintanceDevice
    a, b, c, d, e = cirq.LineQubit.range(5)
    swap = cca.SwapPermutationGate()

    with pytest.raises(TypeError):
        ops = [cca.acquaint(a, b)]
        strategy = cirq.Circuit(ops)
        cca.remove_redundant_acquaintance_opportunities(strategy)

    ops = [cca.acquaint(a, b), cca.acquaint(a, b)]
    strategy = cirq.Circuit(ops, device=device)
    diagram_before = """
0: ───█───█───
      │   │
1: ───█───█───
    """
    ct.assert_has_diagram(strategy, diagram_before)
    cca.remove_redundant_acquaintance_opportunities(strategy)
    cca.remove_redundant_acquaintance_opportunities(strategy)
    diagram_after = """
0: ───█───────
      │
1: ───█───────
    """
    ct.assert_has_diagram(strategy, diagram_after)


    ops = [
            cca.acquaint(a, b), cca.acquaint(c, d),
            swap(d, e), swap(c, d), cca.acquaint(d, e)]
    strategy = cirq.Circuit(ops, device=device)
    diagram_before = """
0: ───█───────────────────
      │
1: ───█───────────────────

2: ───█─────────0↦1───────
      │         │
3: ───█───0↦1───1↦0───█───
          │           │
4: ───────1↦0─────────█───
    """
    ct.assert_has_diagram(strategy, diagram_before)
    cca.remove_redundant_acquaintance_opportunities(strategy)
    diagram_after = """
0: ───█───────────────────
      │
1: ───█───────────────────

2: ───█─────────0↦1───────
      │         │
3: ───█───0↦1───1↦0───────
          │
4: ───────1↦0─────────────
    """
    ct.assert_has_diagram(strategy, diagram_after)

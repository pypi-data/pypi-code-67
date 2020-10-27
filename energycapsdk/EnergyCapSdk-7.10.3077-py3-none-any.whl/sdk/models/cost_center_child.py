# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CostCenterChild(Model):
    """CostCenterChild.

    :param cost_center_id: The cost center identifier
    :type cost_center_id: int
    :param cost_center_code: The cost center code
    :type cost_center_code: str
    :param cost_center_info: The cost center info
    :type cost_center_info: str
    """

    _attribute_map = {
        'cost_center_id': {'key': 'costCenterId', 'type': 'int'},
        'cost_center_code': {'key': 'costCenterCode', 'type': 'str'},
        'cost_center_info': {'key': 'costCenterInfo', 'type': 'str'},
    }

    def __init__(self, cost_center_id=None, cost_center_code=None, cost_center_info=None):
        super(CostCenterChild, self).__init__()
        self.cost_center_id = cost_center_id
        self.cost_center_code = cost_center_code
        self.cost_center_info = cost_center_info

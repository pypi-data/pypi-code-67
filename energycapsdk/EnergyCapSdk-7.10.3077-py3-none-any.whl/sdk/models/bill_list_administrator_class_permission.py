# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillListAdministratorClassPermission(Model):
    """BillListAdministratorClassPermission.

    :param manage:
    :type manage: bool
    """

    _attribute_map = {
        'manage': {'key': 'manage', 'type': 'bool'},
    }

    def __init__(self, manage=None):
        super(BillListAdministratorClassPermission, self).__init__()
        self.manage = manage

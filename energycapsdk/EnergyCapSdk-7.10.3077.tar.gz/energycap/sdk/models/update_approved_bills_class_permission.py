# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UpdateApprovedBillsClassPermission(Model):
    """UpdateApprovedBillsClassPermission.

    :param edit:
    :type edit: bool
    :param delete:
    :type delete: bool
    """

    _attribute_map = {
        'edit': {'key': 'edit', 'type': 'bool'},
        'delete': {'key': 'delete', 'type': 'bool'},
    }

    def __init__(self, edit=None, delete=None):
        super(UpdateApprovedBillsClassPermission, self).__init__()
        self.edit = edit
        self.delete = delete

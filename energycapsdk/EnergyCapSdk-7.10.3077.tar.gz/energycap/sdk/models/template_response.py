# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class TemplateResponse(Model):
    """TemplateResponse.

    :param template_id:
    :type template_id: int
    :param template_code:
    :type template_code: str
    :param template_info:
    :type template_info: str
    :param note:
    :type note: str
    :param commodity:
    :type commodity: ~energycap.sdk.models.CommodityChild
    :param demand_unit:
    :type demand_unit: ~energycap.sdk.models.UnitChild
    :param use_unit:
    :type use_unit: ~energycap.sdk.models.UnitChild
    :param versions:
    :type versions: list[~energycap.sdk.models.VersionChild]
    """

    _attribute_map = {
        'template_id': {'key': 'templateId', 'type': 'int'},
        'template_code': {'key': 'templateCode', 'type': 'str'},
        'template_info': {'key': 'templateInfo', 'type': 'str'},
        'note': {'key': 'note', 'type': 'str'},
        'commodity': {'key': 'commodity', 'type': 'CommodityChild'},
        'demand_unit': {'key': 'demandUnit', 'type': 'UnitChild'},
        'use_unit': {'key': 'useUnit', 'type': 'UnitChild'},
        'versions': {'key': 'versions', 'type': '[VersionChild]'},
    }

    def __init__(self, template_id=None, template_code=None, template_info=None, note=None, commodity=None, demand_unit=None, use_unit=None, versions=None):
        super(TemplateResponse, self).__init__()
        self.template_id = template_id
        self.template_code = template_code
        self.template_info = template_info
        self.note = note
        self.commodity = commodity
        self.demand_unit = demand_unit
        self.use_unit = use_unit
        self.versions = versions

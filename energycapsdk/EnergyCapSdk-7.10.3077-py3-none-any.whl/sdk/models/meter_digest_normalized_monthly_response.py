# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeterDigestNormalizedMonthlyResponse(Model):
    """MeterDigestNormalizedMonthlyResponse.

    :param meter_code: The meter code
    :type meter_code: str
    :param meter_info: The meter info
    :type meter_info: str
    :param meter_id: The meter identifier
    :type meter_id: int
    :param updated: The date and time the data was updated
    :type updated: datetime
    :param native_use_unit:
    :type native_use_unit: ~energycap.sdk.models.UnitChild
    :param native_demand_unit:
    :type native_demand_unit: ~energycap.sdk.models.UnitChild
    :param common_use_unit:
    :type common_use_unit: ~energycap.sdk.models.UnitChild
    :param results: An array of monthly data
    :type results:
     list[~energycap.sdk.models.MeterDigestNormalizedMonthlyResponseResults]
    """

    _attribute_map = {
        'meter_code': {'key': 'meterCode', 'type': 'str'},
        'meter_info': {'key': 'meterInfo', 'type': 'str'},
        'meter_id': {'key': 'meterId', 'type': 'int'},
        'updated': {'key': 'updated', 'type': 'iso-8601'},
        'native_use_unit': {'key': 'nativeUseUnit', 'type': 'UnitChild'},
        'native_demand_unit': {'key': 'nativeDemandUnit', 'type': 'UnitChild'},
        'common_use_unit': {'key': 'commonUseUnit', 'type': 'UnitChild'},
        'results': {'key': 'results', 'type': '[MeterDigestNormalizedMonthlyResponseResults]'},
    }

    def __init__(self, meter_code=None, meter_info=None, meter_id=None, updated=None, native_use_unit=None, native_demand_unit=None, common_use_unit=None, results=None):
        super(MeterDigestNormalizedMonthlyResponse, self).__init__()
        self.meter_code = meter_code
        self.meter_info = meter_info
        self.meter_id = meter_id
        self.updated = updated
        self.native_use_unit = native_use_unit
        self.native_demand_unit = native_demand_unit
        self.common_use_unit = common_use_unit
        self.results = results

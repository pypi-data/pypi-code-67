# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AucRangeResponse(Model):
    """AucRangeResponse.

    :param commodity_cap_id: Unique identifier for the commodity's average
     unit cost range
    :type commodity_cap_id: int
    :param commodity:
    :type commodity: ~energycap.sdk.models.CommodityChild
    :param lower_limit_multiplier: When the current bill's average unit cost
     is LOWER than this multiplier x the baseline bill's average unit cost,
     then the cost avoidance processor will use the average unit cost from the
     baseline bill instead of the current bill
    :type lower_limit_multiplier: float
    :param upper_limit_multiplier: When the current bill's average unit cost
     is HIGHER than this multiplier x the baseline bill's average unit cost,
     then the cost avoidance processor will use the average unit cost from the
     baseline bill instead of the current bill
    :type upper_limit_multiplier: float
    :param is_used: Indicates whether or not this commodity is used; i.e.
     there are meters that have been created with this commodity which are
     included in cost avoidance
    :type is_used: bool
    """

    _attribute_map = {
        'commodity_cap_id': {'key': 'commodityCapId', 'type': 'int'},
        'commodity': {'key': 'commodity', 'type': 'CommodityChild'},
        'lower_limit_multiplier': {'key': 'lowerLimitMultiplier', 'type': 'float'},
        'upper_limit_multiplier': {'key': 'upperLimitMultiplier', 'type': 'float'},
        'is_used': {'key': 'isUsed', 'type': 'bool'},
    }

    def __init__(self, commodity_cap_id=None, commodity=None, lower_limit_multiplier=None, upper_limit_multiplier=None, is_used=None):
        super(AucRangeResponse, self).__init__()
        self.commodity_cap_id = commodity_cap_id
        self.commodity = commodity
        self.lower_limit_multiplier = lower_limit_multiplier
        self.upper_limit_multiplier = upper_limit_multiplier
        self.is_used = is_used

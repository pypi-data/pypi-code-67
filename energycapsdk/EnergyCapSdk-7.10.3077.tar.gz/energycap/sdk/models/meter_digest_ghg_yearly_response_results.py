# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeterDigestGHGYearlyResponseResults(Model):
    """MeterDigestGHGYearlyResponseResults.

    :param year: year
    :type year: str
    :param equivalent_co2_emissions: Equivalent CO2 emissions
    :type equivalent_co2_emissions: float
    """

    _attribute_map = {
        'year': {'key': 'year', 'type': 'str'},
        'equivalent_co2_emissions': {'key': 'equivalentCO2Emissions', 'type': 'float'},
    }

    def __init__(self, year=None, equivalent_co2_emissions=None):
        super(MeterDigestGHGYearlyResponseResults, self).__init__()
        self.year = year
        self.equivalent_co2_emissions = equivalent_co2_emissions

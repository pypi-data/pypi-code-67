# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class WeatherStationChild(Model):
    """WeatherStationChild.

    :param station_id:
    :type station_id: int
    :param station_code:
    :type station_code: str
    :param station_info:
    :type station_info: str
    :param city:
    :type city: str
    :param state:
    :type state: str
    :param country:
    :type country: str
    """

    _attribute_map = {
        'station_id': {'key': 'stationId', 'type': 'int'},
        'station_code': {'key': 'stationCode', 'type': 'str'},
        'station_info': {'key': 'stationInfo', 'type': 'str'},
        'city': {'key': 'city', 'type': 'str'},
        'state': {'key': 'state', 'type': 'str'},
        'country': {'key': 'country', 'type': 'str'},
    }

    def __init__(self, station_id=None, station_code=None, station_info=None, city=None, state=None, country=None):
        super(WeatherStationChild, self).__init__()
        self.station_id = station_id
        self.station_code = station_code
        self.station_info = station_info
        self.city = city
        self.state = state
        self.country = country

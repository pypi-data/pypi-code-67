# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.49.07-BETA
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class SeriesBatchInputV1(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'series': 'list[SeriesInputV1]'
    }

    attribute_map = {
        'series': 'series'
    }

    def __init__(self, series=None):
        """
        SeriesBatchInputV1 - a model defined in Swagger
        """

        self._series = None

        if series is not None:
          self.series = series

    @property
    def series(self):
        """
        Gets the series of this SeriesBatchInputV1.
        A list of series to create or update

        :return: The series of this SeriesBatchInputV1.
        :rtype: list[SeriesInputV1]
        """
        return self._series

    @series.setter
    def series(self, series):
        """
        Sets the series of this SeriesBatchInputV1.
        A list of series to create or update

        :param series: The series of this SeriesBatchInputV1.
        :type: list[SeriesInputV1]
        """
        if series is None:
            raise ValueError("Invalid value for `series`, must not be `None`")

        self._series = series

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, SeriesBatchInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

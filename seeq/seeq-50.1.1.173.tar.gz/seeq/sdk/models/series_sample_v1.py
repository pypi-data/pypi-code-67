# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 50.1.1-BETA
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class SeriesSampleV1(object):
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
        'is_uncertain': 'bool',
        'key': 'object',
        'value': 'object'
    }

    attribute_map = {
        'is_uncertain': 'isUncertain',
        'key': 'key',
        'value': 'value'
    }

    def __init__(self, is_uncertain=None, key=None, value=None):
        """
        SeriesSampleV1 - a model defined in Swagger
        """

        self._is_uncertain = None
        self._key = None
        self._value = None

        if is_uncertain is not None:
          self.is_uncertain = is_uncertain
        if key is not None:
          self.key = key
        if value is not None:
          self.value = value

    @property
    def is_uncertain(self):
        """
        Gets the is_uncertain of this SeriesSampleV1.
        True if this sample is uncertain

        :return: The is_uncertain of this SeriesSampleV1.
        :rtype: bool
        """
        return self._is_uncertain

    @is_uncertain.setter
    def is_uncertain(self, is_uncertain):
        """
        Sets the is_uncertain of this SeriesSampleV1.
        True if this sample is uncertain

        :param is_uncertain: The is_uncertain of this SeriesSampleV1.
        :type: bool
        """

        self._is_uncertain = is_uncertain

    @property
    def key(self):
        """
        Gets the key of this SeriesSampleV1.
        The key of the sample. For a time series, an ISO 8601 date string(YYYY-MM-DDThh:mm:ss.sssssssssÂ±hh:mm). For a numeric (non-time) series, a double-precision number.

        :return: The key of this SeriesSampleV1.
        :rtype: object
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this SeriesSampleV1.
        The key of the sample. For a time series, an ISO 8601 date string(YYYY-MM-DDThh:mm:ss.sssssssssÂ±hh:mm). For a numeric (non-time) series, a double-precision number.

        :param key: The key of this SeriesSampleV1.
        :type: object
        """
        if key is None:
            raise ValueError("Invalid value for `key`, must not be `None`")

        self._key = key

    @property
    def value(self):
        """
        Gets the value of this SeriesSampleV1.
        The value of the sample

        :return: The value of this SeriesSampleV1.
        :rtype: object
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this SeriesSampleV1.
        The value of the sample

        :param value: The value of this SeriesSampleV1.
        :type: object
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")

        self._value = value

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
        if not isinstance(other, SeriesSampleV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

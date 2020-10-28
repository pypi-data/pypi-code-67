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


class SeriesSamplesInputV1(object):
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
        'key_unit_of_measure': 'str',
        'samples': 'list[SeriesSampleV1]',
        'value_unit_of_measure': 'str'
    }

    attribute_map = {
        'key_unit_of_measure': 'keyUnitOfMeasure',
        'samples': 'samples',
        'value_unit_of_measure': 'valueUnitOfMeasure'
    }

    def __init__(self, key_unit_of_measure=None, samples=None, value_unit_of_measure=None):
        """
        SeriesSamplesInputV1 - a model defined in Swagger
        """

        self._key_unit_of_measure = None
        self._samples = None
        self._value_unit_of_measure = None

        if key_unit_of_measure is not None:
          self.key_unit_of_measure = key_unit_of_measure
        if samples is not None:
          self.samples = samples
        if value_unit_of_measure is not None:
          self.value_unit_of_measure = value_unit_of_measure

    @property
    def key_unit_of_measure(self):
        """
        Gets the key_unit_of_measure of this SeriesSamplesInputV1.
        The unit of measure for the series keys

        :return: The key_unit_of_measure of this SeriesSamplesInputV1.
        :rtype: str
        """
        return self._key_unit_of_measure

    @key_unit_of_measure.setter
    def key_unit_of_measure(self, key_unit_of_measure):
        """
        Sets the key_unit_of_measure of this SeriesSamplesInputV1.
        The unit of measure for the series keys

        :param key_unit_of_measure: The key_unit_of_measure of this SeriesSamplesInputV1.
        :type: str
        """

        self._key_unit_of_measure = key_unit_of_measure

    @property
    def samples(self):
        """
        Gets the samples of this SeriesSamplesInputV1.
        The list of samples

        :return: The samples of this SeriesSamplesInputV1.
        :rtype: list[SeriesSampleV1]
        """
        return self._samples

    @samples.setter
    def samples(self, samples):
        """
        Sets the samples of this SeriesSamplesInputV1.
        The list of samples

        :param samples: The samples of this SeriesSamplesInputV1.
        :type: list[SeriesSampleV1]
        """
        if samples is None:
            raise ValueError("Invalid value for `samples`, must not be `None`")

        self._samples = samples

    @property
    def value_unit_of_measure(self):
        """
        Gets the value_unit_of_measure of this SeriesSamplesInputV1.
        The unit of measure for the series values

        :return: The value_unit_of_measure of this SeriesSamplesInputV1.
        :rtype: str
        """
        return self._value_unit_of_measure

    @value_unit_of_measure.setter
    def value_unit_of_measure(self, value_unit_of_measure):
        """
        Sets the value_unit_of_measure of this SeriesSamplesInputV1.
        The unit of measure for the series values

        :param value_unit_of_measure: The value_unit_of_measure of this SeriesSamplesInputV1.
        :type: str
        """

        self._value_unit_of_measure = value_unit_of_measure

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
        if not isinstance(other, SeriesSamplesInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

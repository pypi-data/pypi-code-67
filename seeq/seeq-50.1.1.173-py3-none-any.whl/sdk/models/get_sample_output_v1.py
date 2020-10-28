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


class GetSampleOutputV1(object):
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
        'sample': 'SampleOutputV1',
        'status_message': 'str',
        'value_unit_of_measure': 'str'
    }

    attribute_map = {
        'key_unit_of_measure': 'keyUnitOfMeasure',
        'sample': 'sample',
        'status_message': 'statusMessage',
        'value_unit_of_measure': 'valueUnitOfMeasure'
    }

    def __init__(self, key_unit_of_measure=None, sample=None, status_message=None, value_unit_of_measure=None):
        """
        GetSampleOutputV1 - a model defined in Swagger
        """

        self._key_unit_of_measure = None
        self._sample = None
        self._status_message = None
        self._value_unit_of_measure = None

        if key_unit_of_measure is not None:
          self.key_unit_of_measure = key_unit_of_measure
        if sample is not None:
          self.sample = sample
        if status_message is not None:
          self.status_message = status_message
        if value_unit_of_measure is not None:
          self.value_unit_of_measure = value_unit_of_measure

    @property
    def key_unit_of_measure(self):
        """
        Gets the key_unit_of_measure of this GetSampleOutputV1.
        The unit of measure for the signal's keys. A time-keyed signal has key units of 'ns'.

        :return: The key_unit_of_measure of this GetSampleOutputV1.
        :rtype: str
        """
        return self._key_unit_of_measure

    @key_unit_of_measure.setter
    def key_unit_of_measure(self, key_unit_of_measure):
        """
        Sets the key_unit_of_measure of this GetSampleOutputV1.
        The unit of measure for the signal's keys. A time-keyed signal has key units of 'ns'.

        :param key_unit_of_measure: The key_unit_of_measure of this GetSampleOutputV1.
        :type: str
        """

        self._key_unit_of_measure = key_unit_of_measure

    @property
    def sample(self):
        """
        Gets the sample of this GetSampleOutputV1.
        The sample, or null if no sample was found

        :return: The sample of this GetSampleOutputV1.
        :rtype: SampleOutputV1
        """
        return self._sample

    @sample.setter
    def sample(self, sample):
        """
        Sets the sample of this GetSampleOutputV1.
        The sample, or null if no sample was found

        :param sample: The sample of this GetSampleOutputV1.
        :type: SampleOutputV1
        """

        self._sample = sample

    @property
    def status_message(self):
        """
        Gets the status_message of this GetSampleOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation. Null if the status message has not been set.

        :return: The status_message of this GetSampleOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this GetSampleOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation. Null if the status message has not been set.

        :param status_message: The status_message of this GetSampleOutputV1.
        :type: str
        """

        self._status_message = status_message

    @property
    def value_unit_of_measure(self):
        """
        Gets the value_unit_of_measure of this GetSampleOutputV1.
        The unit of measure for the signal's values

        :return: The value_unit_of_measure of this GetSampleOutputV1.
        :rtype: str
        """
        return self._value_unit_of_measure

    @value_unit_of_measure.setter
    def value_unit_of_measure(self, value_unit_of_measure):
        """
        Sets the value_unit_of_measure of this GetSampleOutputV1.
        The unit of measure for the signal's values

        :param value_unit_of_measure: The value_unit_of_measure of this GetSampleOutputV1.
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
        if not isinstance(other, GetSampleOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

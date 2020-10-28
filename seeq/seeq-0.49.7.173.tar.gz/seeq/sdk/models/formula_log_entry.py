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


class FormulaLogEntry(object):
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
        'log_details': 'list[FormulaLogEntryDetails]',
        'log_type_count': 'int'
    }

    attribute_map = {
        'log_details': 'logDetails',
        'log_type_count': 'logTypeCount'
    }

    def __init__(self, log_details=None, log_type_count=None):
        """
        FormulaLogEntry - a model defined in Swagger
        """

        self._log_details = None
        self._log_type_count = None

        if log_details is not None:
          self.log_details = log_details
        if log_type_count is not None:
          self.log_type_count = log_type_count

    @property
    def log_details(self):
        """
        Gets the log_details of this FormulaLogEntry.

        :return: The log_details of this FormulaLogEntry.
        :rtype: list[FormulaLogEntryDetails]
        """
        return self._log_details

    @log_details.setter
    def log_details(self, log_details):
        """
        Sets the log_details of this FormulaLogEntry.

        :param log_details: The log_details of this FormulaLogEntry.
        :type: list[FormulaLogEntryDetails]
        """

        self._log_details = log_details

    @property
    def log_type_count(self):
        """
        Gets the log_type_count of this FormulaLogEntry.

        :return: The log_type_count of this FormulaLogEntry.
        :rtype: int
        """
        return self._log_type_count

    @log_type_count.setter
    def log_type_count(self, log_type_count):
        """
        Sets the log_type_count of this FormulaLogEntry.

        :param log_type_count: The log_type_count of this FormulaLogEntry.
        :type: int
        """

        self._log_type_count = log_type_count

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
        if not isinstance(other, FormulaLogEntry):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.48.10-BETA
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class GenericTableOutputV1(object):
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
        'data': 'list[list[object]]',
        'headers': 'list[TableColumnOutputV1]'
    }

    attribute_map = {
        'data': 'data',
        'headers': 'headers'
    }

    def __init__(self, data=None, headers=None):
        """
        GenericTableOutputV1 - a model defined in Swagger
        """

        self._data = None
        self._headers = None

        if data is not None:
          self.data = data
        if headers is not None:
          self.headers = headers

    @property
    def data(self):
        """
        Gets the data of this GenericTableOutputV1.
        The list of data rows, each row being a list of cell contents.

        :return: The data of this GenericTableOutputV1.
        :rtype: list[list[object]]
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this GenericTableOutputV1.
        The list of data rows, each row being a list of cell contents.

        :param data: The data of this GenericTableOutputV1.
        :type: list[list[object]]
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")

        self._data = data

    @property
    def headers(self):
        """
        Gets the headers of this GenericTableOutputV1.
        The list of headers.

        :return: The headers of this GenericTableOutputV1.
        :rtype: list[TableColumnOutputV1]
        """
        return self._headers

    @headers.setter
    def headers(self, headers):
        """
        Sets the headers of this GenericTableOutputV1.
        The list of headers.

        :param headers: The headers of this GenericTableOutputV1.
        :type: list[TableColumnOutputV1]
        """
        if headers is None:
            raise ValueError("Invalid value for `headers`, must not be `None`")

        self._headers = headers

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
        if not isinstance(other, GenericTableOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

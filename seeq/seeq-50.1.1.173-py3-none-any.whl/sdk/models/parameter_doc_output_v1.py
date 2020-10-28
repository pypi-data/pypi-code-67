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


class ParameterDocOutputV1(object):
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
        'default_value': 'str',
        'description': 'str',
        'name': 'str',
        'optional': 'bool',
        'type': 'str'
    }

    attribute_map = {
        'default_value': 'defaultValue',
        'description': 'description',
        'name': 'name',
        'optional': 'optional',
        'type': 'type'
    }

    def __init__(self, default_value=None, description=None, name=None, optional=False, type=None):
        """
        ParameterDocOutputV1 - a model defined in Swagger
        """

        self._default_value = None
        self._description = None
        self._name = None
        self._optional = None
        self._type = None

        if default_value is not None:
          self.default_value = default_value
        if description is not None:
          self.description = description
        if name is not None:
          self.name = name
        if optional is not None:
          self.optional = optional
        if type is not None:
          self.type = type

    @property
    def default_value(self):
        """
        Gets the default_value of this ParameterDocOutputV1.
        The value to be used if not provided to the function

        :return: The default_value of this ParameterDocOutputV1.
        :rtype: str
        """
        return self._default_value

    @default_value.setter
    def default_value(self, default_value):
        """
        Sets the default_value of this ParameterDocOutputV1.
        The value to be used if not provided to the function

        :param default_value: The default_value of this ParameterDocOutputV1.
        :type: str
        """

        self._default_value = default_value

    @property
    def description(self):
        """
        Gets the description of this ParameterDocOutputV1.
        The description of the parameter

        :return: The description of this ParameterDocOutputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ParameterDocOutputV1.
        The description of the parameter

        :param description: The description of this ParameterDocOutputV1.
        :type: str
        """

        self._description = description

    @property
    def name(self):
        """
        Gets the name of this ParameterDocOutputV1.
        The identifier of the parameter

        :return: The name of this ParameterDocOutputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ParameterDocOutputV1.
        The identifier of the parameter

        :param name: The name of this ParameterDocOutputV1.
        :type: str
        """

        self._name = name

    @property
    def optional(self):
        """
        Gets the optional of this ParameterDocOutputV1.
        Indicate this parameter is optional for the function call

        :return: The optional of this ParameterDocOutputV1.
        :rtype: bool
        """
        return self._optional

    @optional.setter
    def optional(self, optional):
        """
        Sets the optional of this ParameterDocOutputV1.
        Indicate this parameter is optional for the function call

        :param optional: The optional of this ParameterDocOutputV1.
        :type: bool
        """

        self._optional = optional

    @property
    def type(self):
        """
        Gets the type of this ParameterDocOutputV1.
        The type of the parameter

        :return: The type of this ParameterDocOutputV1.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ParameterDocOutputV1.
        The type of the parameter

        :param type: The type of this ParameterDocOutputV1.
        :type: str
        """

        self._type = type

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
        if not isinstance(other, ParameterDocOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

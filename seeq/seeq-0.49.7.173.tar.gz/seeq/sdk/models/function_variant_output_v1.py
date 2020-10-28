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


class FunctionVariantOutputV1(object):
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
        'description': 'str',
        'fluent': 'bool',
        'name': 'str',
        'parameters': 'list[FunctionParameterOutputV1]',
        'return_type': 'str'
    }

    attribute_map = {
        'description': 'description',
        'fluent': 'fluent',
        'name': 'name',
        'parameters': 'parameters',
        'return_type': 'returnType'
    }

    def __init__(self, description=None, fluent=False, name=None, parameters=None, return_type=None):
        """
        FunctionVariantOutputV1 - a model defined in Swagger
        """

        self._description = None
        self._fluent = None
        self._name = None
        self._parameters = None
        self._return_type = None

        if description is not None:
          self.description = description
        if fluent is not None:
          self.fluent = fluent
        if name is not None:
          self.name = name
        if parameters is not None:
          self.parameters = parameters
        if return_type is not None:
          self.return_type = return_type

    @property
    def description(self):
        """
        Gets the description of this FunctionVariantOutputV1.
        The description of the function

        :return: The description of this FunctionVariantOutputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FunctionVariantOutputV1.
        The description of the function

        :param description: The description of this FunctionVariantOutputV1.
        :type: str
        """

        self._description = description

    @property
    def fluent(self):
        """
        Gets the fluent of this FunctionVariantOutputV1.
        True if this function is written in the fluent style

        :return: The fluent of this FunctionVariantOutputV1.
        :rtype: bool
        """
        return self._fluent

    @fluent.setter
    def fluent(self, fluent):
        """
        Sets the fluent of this FunctionVariantOutputV1.
        True if this function is written in the fluent style

        :param fluent: The fluent of this FunctionVariantOutputV1.
        :type: bool
        """

        self._fluent = fluent

    @property
    def name(self):
        """
        Gets the name of this FunctionVariantOutputV1.
        The name of the function

        :return: The name of this FunctionVariantOutputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FunctionVariantOutputV1.
        The name of the function

        :param name: The name of this FunctionVariantOutputV1.
        :type: str
        """

        self._name = name

    @property
    def parameters(self):
        """
        Gets the parameters of this FunctionVariantOutputV1.
        The parameters of the function

        :return: The parameters of this FunctionVariantOutputV1.
        :rtype: list[FunctionParameterOutputV1]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this FunctionVariantOutputV1.
        The parameters of the function

        :param parameters: The parameters of this FunctionVariantOutputV1.
        :type: list[FunctionParameterOutputV1]
        """

        self._parameters = parameters

    @property
    def return_type(self):
        """
        Gets the return_type of this FunctionVariantOutputV1.
        The type of the function

        :return: The return_type of this FunctionVariantOutputV1.
        :rtype: str
        """
        return self._return_type

    @return_type.setter
    def return_type(self, return_type):
        """
        Sets the return_type of this FunctionVariantOutputV1.
        The type of the function

        :param return_type: The return_type of this FunctionVariantOutputV1.
        :type: str
        """

        self._return_type = return_type

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
        if not isinstance(other, FunctionVariantOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

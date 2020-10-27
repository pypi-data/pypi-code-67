# coding: utf-8

"""
    Red Rover API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1
    Contact: contact@edustaff.org
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from redrover_api.configuration import Configuration


class MethodImplAttributes(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    _0 = "0"
    _1 = "1"
    _2 = "2"
    _3 = "3"
    _4 = "4"
    _8 = "8"
    _16 = "16"
    _32 = "32"
    _64 = "64"
    _128 = "128"
    _256 = "256"
    _512 = "512"
    _4096 = "4096"
    _65535 = "65535"

    allowable_values = [_0, _1, _2, _3, _4, _8, _16, _32, _64, _128, _256, _512, _4096, _65535]  # noqa: E501

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
    }

    attribute_map = {
    }

    def __init__(self, local_vars_configuration=None):  # noqa: E501
        """MethodImplAttributes - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration
        self.discriminator = None

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MethodImplAttributes):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MethodImplAttributes):
            return True

        return self.to_dict() != other.to_dict()

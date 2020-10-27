# coding: utf-8

"""
    Managed Ray API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class SessionStartingUpData(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'startup_progress': 'str',
        'startup_error': 'str'
    }

    attribute_map = {
        'startup_progress': 'startup_progress',
        'startup_error': 'startup_error'
    }

    def __init__(self, startup_progress=None, startup_error=None, local_vars_configuration=None):  # noqa: E501
        """SessionStartingUpData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._startup_progress = None
        self._startup_error = None
        self.discriminator = None

        if startup_progress is not None:
            self.startup_progress = startup_progress
        if startup_error is not None:
            self.startup_error = startup_error

    @property
    def startup_progress(self):
        """Gets the startup_progress of this SessionStartingUpData.  # noqa: E501


        :return: The startup_progress of this SessionStartingUpData.  # noqa: E501
        :rtype: str
        """
        return self._startup_progress

    @startup_progress.setter
    def startup_progress(self, startup_progress):
        """Sets the startup_progress of this SessionStartingUpData.


        :param startup_progress: The startup_progress of this SessionStartingUpData.  # noqa: E501
        :type: str
        """

        self._startup_progress = startup_progress

    @property
    def startup_error(self):
        """Gets the startup_error of this SessionStartingUpData.  # noqa: E501


        :return: The startup_error of this SessionStartingUpData.  # noqa: E501
        :rtype: str
        """
        return self._startup_error

    @startup_error.setter
    def startup_error(self, startup_error):
        """Sets the startup_error of this SessionStartingUpData.


        :param startup_error: The startup_error of this SessionStartingUpData.  # noqa: E501
        :type: str
        """

        self._startup_error = startup_error

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
        if not isinstance(other, SessionStartingUpData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SessionStartingUpData):
            return True

        return self.to_dict() != other.to_dict()

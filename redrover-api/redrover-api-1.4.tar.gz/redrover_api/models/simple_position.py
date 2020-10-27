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


class SimplePosition(object):
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
        'id': 'int',
        'title': 'str',
        'hours_per_full_work_day': 'float'
    }

    attribute_map = {
        'id': 'id',
        'title': 'title',
        'hours_per_full_work_day': 'hoursPerFullWorkDay'
    }

    def __init__(self, id=None, title=None, hours_per_full_work_day=None, local_vars_configuration=None):  # noqa: E501
        """SimplePosition - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._title = None
        self._hours_per_full_work_day = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.title = title
        self.hours_per_full_work_day = hours_per_full_work_day

    @property
    def id(self):
        """Gets the id of this SimplePosition.  # noqa: E501


        :return: The id of this SimplePosition.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SimplePosition.


        :param id: The id of this SimplePosition.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def title(self):
        """Gets the title of this SimplePosition.  # noqa: E501


        :return: The title of this SimplePosition.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this SimplePosition.


        :param title: The title of this SimplePosition.  # noqa: E501
        :type title: str
        """

        self._title = title

    @property
    def hours_per_full_work_day(self):
        """Gets the hours_per_full_work_day of this SimplePosition.  # noqa: E501


        :return: The hours_per_full_work_day of this SimplePosition.  # noqa: E501
        :rtype: float
        """
        return self._hours_per_full_work_day

    @hours_per_full_work_day.setter
    def hours_per_full_work_day(self, hours_per_full_work_day):
        """Sets the hours_per_full_work_day of this SimplePosition.


        :param hours_per_full_work_day: The hours_per_full_work_day of this SimplePosition.  # noqa: E501
        :type hours_per_full_work_day: float
        """

        self._hours_per_full_work_day = hours_per_full_work_day

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
        if not isinstance(other, SimplePosition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SimplePosition):
            return True

        return self.to_dict() != other.to_dict()

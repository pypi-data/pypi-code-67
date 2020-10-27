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


class PositionScheduleDto(object):
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
        'items': 'list[PositionScheduleItemDto]',
        'days_of_the_week': 'list[DayOfWeek]',
        'skip_concurrency_check': 'bool',
        'provided_properties': 'list[PropertyInfo]'
    }

    attribute_map = {
        'items': 'items',
        'days_of_the_week': 'daysOfTheWeek',
        'skip_concurrency_check': 'skipConcurrencyCheck',
        'provided_properties': 'providedProperties'
    }

    def __init__(self, items=None, days_of_the_week=None, skip_concurrency_check=None, provided_properties=None, local_vars_configuration=None):  # noqa: E501
        """PositionScheduleDto - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._items = None
        self._days_of_the_week = None
        self._skip_concurrency_check = None
        self._provided_properties = None
        self.discriminator = None

        self.items = items
        self.days_of_the_week = days_of_the_week
        if skip_concurrency_check is not None:
            self.skip_concurrency_check = skip_concurrency_check
        self.provided_properties = provided_properties

    @property
    def items(self):
        """Gets the items of this PositionScheduleDto.  # noqa: E501


        :return: The items of this PositionScheduleDto.  # noqa: E501
        :rtype: list[PositionScheduleItemDto]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this PositionScheduleDto.


        :param items: The items of this PositionScheduleDto.  # noqa: E501
        :type items: list[PositionScheduleItemDto]
        """

        self._items = items

    @property
    def days_of_the_week(self):
        """Gets the days_of_the_week of this PositionScheduleDto.  # noqa: E501


        :return: The days_of_the_week of this PositionScheduleDto.  # noqa: E501
        :rtype: list[DayOfWeek]
        """
        return self._days_of_the_week

    @days_of_the_week.setter
    def days_of_the_week(self, days_of_the_week):
        """Sets the days_of_the_week of this PositionScheduleDto.


        :param days_of_the_week: The days_of_the_week of this PositionScheduleDto.  # noqa: E501
        :type days_of_the_week: list[DayOfWeek]
        """

        self._days_of_the_week = days_of_the_week

    @property
    def skip_concurrency_check(self):
        """Gets the skip_concurrency_check of this PositionScheduleDto.  # noqa: E501


        :return: The skip_concurrency_check of this PositionScheduleDto.  # noqa: E501
        :rtype: bool
        """
        return self._skip_concurrency_check

    @skip_concurrency_check.setter
    def skip_concurrency_check(self, skip_concurrency_check):
        """Sets the skip_concurrency_check of this PositionScheduleDto.


        :param skip_concurrency_check: The skip_concurrency_check of this PositionScheduleDto.  # noqa: E501
        :type skip_concurrency_check: bool
        """

        self._skip_concurrency_check = skip_concurrency_check

    @property
    def provided_properties(self):
        """Gets the provided_properties of this PositionScheduleDto.  # noqa: E501


        :return: The provided_properties of this PositionScheduleDto.  # noqa: E501
        :rtype: list[PropertyInfo]
        """
        return self._provided_properties

    @provided_properties.setter
    def provided_properties(self, provided_properties):
        """Sets the provided_properties of this PositionScheduleDto.


        :param provided_properties: The provided_properties of this PositionScheduleDto.  # noqa: E501
        :type provided_properties: list[PropertyInfo]
        """

        self._provided_properties = provided_properties

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
        if not isinstance(other, PositionScheduleDto):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PositionScheduleDto):
            return True

        return self.to_dict() != other.to_dict()

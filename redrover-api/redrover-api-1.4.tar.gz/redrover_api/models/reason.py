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


class Reason(object):
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
        'vacancy_reason_id': 'int',
        'absence_reason_id': 'int',
        'external_id': 'str',
        'name': 'str'
    }

    attribute_map = {
        'vacancy_reason_id': 'vacancyReasonId',
        'absence_reason_id': 'absenceReasonId',
        'external_id': 'externalId',
        'name': 'name'
    }

    def __init__(self, vacancy_reason_id=None, absence_reason_id=None, external_id=None, name=None, local_vars_configuration=None):  # noqa: E501
        """Reason - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._vacancy_reason_id = None
        self._absence_reason_id = None
        self._external_id = None
        self._name = None
        self.discriminator = None

        if vacancy_reason_id is not None:
            self.vacancy_reason_id = vacancy_reason_id
        if absence_reason_id is not None:
            self.absence_reason_id = absence_reason_id
        self.external_id = external_id
        self.name = name

    @property
    def vacancy_reason_id(self):
        """Gets the vacancy_reason_id of this Reason.  # noqa: E501


        :return: The vacancy_reason_id of this Reason.  # noqa: E501
        :rtype: int
        """
        return self._vacancy_reason_id

    @vacancy_reason_id.setter
    def vacancy_reason_id(self, vacancy_reason_id):
        """Sets the vacancy_reason_id of this Reason.


        :param vacancy_reason_id: The vacancy_reason_id of this Reason.  # noqa: E501
        :type vacancy_reason_id: int
        """

        self._vacancy_reason_id = vacancy_reason_id

    @property
    def absence_reason_id(self):
        """Gets the absence_reason_id of this Reason.  # noqa: E501


        :return: The absence_reason_id of this Reason.  # noqa: E501
        :rtype: int
        """
        return self._absence_reason_id

    @absence_reason_id.setter
    def absence_reason_id(self, absence_reason_id):
        """Sets the absence_reason_id of this Reason.


        :param absence_reason_id: The absence_reason_id of this Reason.  # noqa: E501
        :type absence_reason_id: int
        """

        self._absence_reason_id = absence_reason_id

    @property
    def external_id(self):
        """Gets the external_id of this Reason.  # noqa: E501


        :return: The external_id of this Reason.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """Sets the external_id of this Reason.


        :param external_id: The external_id of this Reason.  # noqa: E501
        :type external_id: str
        """

        self._external_id = external_id

    @property
    def name(self):
        """Gets the name of this Reason.  # noqa: E501


        :return: The name of this Reason.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Reason.


        :param name: The name of this Reason.  # noqa: E501
        :type name: str
        """

        self._name = name

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
        if not isinstance(other, Reason):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Reason):
            return True

        return self.to_dict() != other.to_dict()

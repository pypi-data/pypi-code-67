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


class PutUserGroupsInputV1(object):
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
        'user_groups': 'list[UserGroupWithIdInputV1]'
    }

    attribute_map = {
        'user_groups': 'userGroups'
    }

    def __init__(self, user_groups=None):
        """
        PutUserGroupsInputV1 - a model defined in Swagger
        """

        self._user_groups = None

        if user_groups is not None:
          self.user_groups = user_groups

    @property
    def user_groups(self):
        """
        Gets the user_groups of this PutUserGroupsInputV1.
        The user groups to create or update

        :return: The user_groups of this PutUserGroupsInputV1.
        :rtype: list[UserGroupWithIdInputV1]
        """
        return self._user_groups

    @user_groups.setter
    def user_groups(self, user_groups):
        """
        Sets the user_groups of this PutUserGroupsInputV1.
        The user groups to create or update

        :param user_groups: The user_groups of this PutUserGroupsInputV1.
        :type: list[UserGroupWithIdInputV1]
        """
        if user_groups is None:
            raise ValueError("Invalid value for `user_groups`, must not be `None`")

        self._user_groups = user_groups

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
        if not isinstance(other, PutUserGroupsInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

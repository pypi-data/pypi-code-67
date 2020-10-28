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


class UserGroupWithIdInputV1(object):
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
        'data_id': 'str',
        'datasource_class': 'str',
        'datasource_id': 'str',
        'description': 'str',
        'is_enabled': 'bool',
        'mapping': 'bool',
        'mappings': 'IdentityMappingListV1',
        'name': 'str',
        'remove_permissions': 'bool',
        'sync_token': 'str'
    }

    attribute_map = {
        'data_id': 'dataId',
        'datasource_class': 'datasourceClass',
        'datasource_id': 'datasourceId',
        'description': 'description',
        'is_enabled': 'isEnabled',
        'mapping': 'mapping',
        'mappings': 'mappings',
        'name': 'name',
        'remove_permissions': 'removePermissions',
        'sync_token': 'syncToken'
    }

    def __init__(self, data_id=None, datasource_class=None, datasource_id=None, description=None, is_enabled=True, mapping=False, mappings=None, name=None, remove_permissions=False, sync_token=None):
        """
        UserGroupWithIdInputV1 - a model defined in Swagger
        """

        self._data_id = None
        self._datasource_class = None
        self._datasource_id = None
        self._description = None
        self._is_enabled = None
        self._mapping = None
        self._mappings = None
        self._name = None
        self._remove_permissions = None
        self._sync_token = None

        if data_id is not None:
          self.data_id = data_id
        if datasource_class is not None:
          self.datasource_class = datasource_class
        if datasource_id is not None:
          self.datasource_id = datasource_id
        if description is not None:
          self.description = description
        if is_enabled is not None:
          self.is_enabled = is_enabled
        if mapping is not None:
          self.mapping = mapping
        if mappings is not None:
          self.mappings = mappings
        if name is not None:
          self.name = name
        if remove_permissions is not None:
          self.remove_permissions = remove_permissions
        if sync_token is not None:
          self.sync_token = sync_token

    @property
    def data_id(self):
        """
        Gets the data_id of this UserGroupWithIdInputV1.
        A unique identifier for the user group within its datasource.

        :return: The data_id of this UserGroupWithIdInputV1.
        :rtype: str
        """
        return self._data_id

    @data_id.setter
    def data_id(self, data_id):
        """
        Sets the data_id of this UserGroupWithIdInputV1.
        A unique identifier for the user group within its datasource.

        :param data_id: The data_id of this UserGroupWithIdInputV1.
        :type: str
        """

        self._data_id = data_id

    @property
    def datasource_class(self):
        """
        Gets the datasource_class of this UserGroupWithIdInputV1.
        Along with the Datasource ID, the Datasource Class uniquely identifies a datasource. For example, a datasource may be a particular instance of an Active Directory.

        :return: The datasource_class of this UserGroupWithIdInputV1.
        :rtype: str
        """
        return self._datasource_class

    @datasource_class.setter
    def datasource_class(self, datasource_class):
        """
        Sets the datasource_class of this UserGroupWithIdInputV1.
        Along with the Datasource ID, the Datasource Class uniquely identifies a datasource. For example, a datasource may be a particular instance of an Active Directory.

        :param datasource_class: The datasource_class of this UserGroupWithIdInputV1.
        :type: str
        """

        self._datasource_class = datasource_class

    @property
    def datasource_id(self):
        """
        Gets the datasource_id of this UserGroupWithIdInputV1.
        Along with the Datasource Class, the Datasource ID uniquely identifies a datasource. For example, a datasource may be a particular instance of an Active Directory.

        :return: The datasource_id of this UserGroupWithIdInputV1.
        :rtype: str
        """
        return self._datasource_id

    @datasource_id.setter
    def datasource_id(self, datasource_id):
        """
        Sets the datasource_id of this UserGroupWithIdInputV1.
        Along with the Datasource Class, the Datasource ID uniquely identifies a datasource. For example, a datasource may be a particular instance of an Active Directory.

        :param datasource_id: The datasource_id of this UserGroupWithIdInputV1.
        :type: str
        """

        self._datasource_id = datasource_id

    @property
    def description(self):
        """
        Gets the description of this UserGroupWithIdInputV1.
        Clarifying information or other plain language description of this item. An input of just whitespace is equivalent to a null input.

        :return: The description of this UserGroupWithIdInputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UserGroupWithIdInputV1.
        Clarifying information or other plain language description of this item. An input of just whitespace is equivalent to a null input.

        :param description: The description of this UserGroupWithIdInputV1.
        :type: str
        """

        self._description = description

    @property
    def is_enabled(self):
        """
        Gets the is_enabled of this UserGroupWithIdInputV1.
        Whether the user group is enabled or disabled (default true).

        :return: The is_enabled of this UserGroupWithIdInputV1.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this UserGroupWithIdInputV1.
        Whether the user group is enabled or disabled (default true).

        :param is_enabled: The is_enabled of this UserGroupWithIdInputV1.
        :type: bool
        """

        self._is_enabled = is_enabled

    @property
    def mapping(self):
        """
        Gets the mapping of this UserGroupWithIdInputV1.

        :return: The mapping of this UserGroupWithIdInputV1.
        :rtype: bool
        """
        return self._mapping

    @mapping.setter
    def mapping(self, mapping):
        """
        Sets the mapping of this UserGroupWithIdInputV1.

        :param mapping: The mapping of this UserGroupWithIdInputV1.
        :type: bool
        """

        self._mapping = mapping

    @property
    def mappings(self):
        """
        Gets the mappings of this UserGroupWithIdInputV1.
        The list of members that are contained within a synced UserGroup. Use null if the group is being created or updated manually.

        :return: The mappings of this UserGroupWithIdInputV1.
        :rtype: IdentityMappingListV1
        """
        return self._mappings

    @mappings.setter
    def mappings(self, mappings):
        """
        Sets the mappings of this UserGroupWithIdInputV1.
        The list of members that are contained within a synced UserGroup. Use null if the group is being created or updated manually.

        :param mappings: The mappings of this UserGroupWithIdInputV1.
        :type: IdentityMappingListV1
        """

        self._mappings = mappings

    @property
    def name(self):
        """
        Gets the name of this UserGroupWithIdInputV1.
        Human readable name. Required during creation. An input of just whitespaces is equivalent to a null input.

        :return: The name of this UserGroupWithIdInputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UserGroupWithIdInputV1.
        Human readable name. Required during creation. An input of just whitespaces is equivalent to a null input.

        :param name: The name of this UserGroupWithIdInputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def remove_permissions(self):
        """
        Gets the remove_permissions of this UserGroupWithIdInputV1.
        Whether permissions associated with the group should be removed when disabling the group (default false).

        :return: The remove_permissions of this UserGroupWithIdInputV1.
        :rtype: bool
        """
        return self._remove_permissions

    @remove_permissions.setter
    def remove_permissions(self, remove_permissions):
        """
        Sets the remove_permissions of this UserGroupWithIdInputV1.
        Whether permissions associated with the group should be removed when disabling the group (default false).

        :param remove_permissions: The remove_permissions of this UserGroupWithIdInputV1.
        :type: bool
        """

        self._remove_permissions = remove_permissions

    @property
    def sync_token(self):
        """
        Gets the sync_token of this UserGroupWithIdInputV1.
        An arbitrary token (often a date or random ID) that is used during metadata syncs. At the end of a full sync, items with mismatching sync tokens are identified as stale and may be archived using the Datasources clean-up API.

        :return: The sync_token of this UserGroupWithIdInputV1.
        :rtype: str
        """
        return self._sync_token

    @sync_token.setter
    def sync_token(self, sync_token):
        """
        Sets the sync_token of this UserGroupWithIdInputV1.
        An arbitrary token (often a date or random ID) that is used during metadata syncs. At the end of a full sync, items with mismatching sync tokens are identified as stale and may be archived using the Datasources clean-up API.

        :param sync_token: The sync_token of this UserGroupWithIdInputV1.
        :type: str
        """

        self._sync_token = sync_token

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
        if not isinstance(other, UserGroupWithIdInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

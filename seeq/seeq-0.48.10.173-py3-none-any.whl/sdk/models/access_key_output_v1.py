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


class AccessKeyOutputV1(object):
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
        'created_at': 'str',
        'description': 'str',
        'effective_permissions': 'PermissionsV1',
        'href': 'str',
        'id': 'str',
        'is_admin': 'bool',
        'is_archived': 'bool',
        'is_redacted': 'bool',
        'key_id': 'str',
        'last_used': 'str',
        'name': 'str',
        'password': 'str',
        'status_message': 'str',
        'type': 'str',
        'user_id': 'str'
    }

    attribute_map = {
        'created_at': 'createdAt',
        'description': 'description',
        'effective_permissions': 'effectivePermissions',
        'href': 'href',
        'id': 'id',
        'is_admin': 'isAdmin',
        'is_archived': 'isArchived',
        'is_redacted': 'isRedacted',
        'key_id': 'keyId',
        'last_used': 'lastUsed',
        'name': 'name',
        'password': 'password',
        'status_message': 'statusMessage',
        'type': 'type',
        'user_id': 'userId'
    }

    def __init__(self, created_at=None, description=None, effective_permissions=None, href=None, id=None, is_admin=False, is_archived=False, is_redacted=False, key_id=None, last_used=None, name=None, password=None, status_message=None, type=None, user_id=None):
        """
        AccessKeyOutputV1 - a model defined in Swagger
        """

        self._created_at = None
        self._description = None
        self._effective_permissions = None
        self._href = None
        self._id = None
        self._is_admin = None
        self._is_archived = None
        self._is_redacted = None
        self._key_id = None
        self._last_used = None
        self._name = None
        self._password = None
        self._status_message = None
        self._type = None
        self._user_id = None

        if created_at is not None:
          self.created_at = created_at
        if description is not None:
          self.description = description
        if effective_permissions is not None:
          self.effective_permissions = effective_permissions
        if href is not None:
          self.href = href
        if id is not None:
          self.id = id
        if is_admin is not None:
          self.is_admin = is_admin
        if is_archived is not None:
          self.is_archived = is_archived
        if is_redacted is not None:
          self.is_redacted = is_redacted
        if key_id is not None:
          self.key_id = key_id
        if last_used is not None:
          self.last_used = last_used
        if name is not None:
          self.name = name
        if password is not None:
          self.password = password
        if status_message is not None:
          self.status_message = status_message
        if type is not None:
          self.type = type
        if user_id is not None:
          self.user_id = user_id

    @property
    def created_at(self):
        """
        Gets the created_at of this AccessKeyOutputV1.
        The date this API Key was created

        :return: The created_at of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this AccessKeyOutputV1.
        The date this API Key was created

        :param created_at: The created_at of this AccessKeyOutputV1.
        :type: str
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")

        self._created_at = created_at

    @property
    def description(self):
        """
        Gets the description of this AccessKeyOutputV1.
        Clarifying information or other plain language description of this item

        :return: The description of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this AccessKeyOutputV1.
        Clarifying information or other plain language description of this item

        :param description: The description of this AccessKeyOutputV1.
        :type: str
        """

        self._description = description

    @property
    def effective_permissions(self):
        """
        Gets the effective_permissions of this AccessKeyOutputV1.
        The permissions the current user has to the item.

        :return: The effective_permissions of this AccessKeyOutputV1.
        :rtype: PermissionsV1
        """
        return self._effective_permissions

    @effective_permissions.setter
    def effective_permissions(self, effective_permissions):
        """
        Sets the effective_permissions of this AccessKeyOutputV1.
        The permissions the current user has to the item.

        :param effective_permissions: The effective_permissions of this AccessKeyOutputV1.
        :type: PermissionsV1
        """

        self._effective_permissions = effective_permissions

    @property
    def href(self):
        """
        Gets the href of this AccessKeyOutputV1.
        The href that can be used to interact with the item

        :return: The href of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """
        Sets the href of this AccessKeyOutputV1.
        The href that can be used to interact with the item

        :param href: The href of this AccessKeyOutputV1.
        :type: str
        """
        if href is None:
            raise ValueError("Invalid value for `href`, must not be `None`")

        self._href = href

    @property
    def id(self):
        """
        Gets the id of this AccessKeyOutputV1.
        The ID that can be used to interact with the item

        :return: The id of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AccessKeyOutputV1.
        The ID that can be used to interact with the item

        :param id: The id of this AccessKeyOutputV1.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def is_admin(self):
        """
        Gets the is_admin of this AccessKeyOutputV1.
        Is Admin Capable

        :return: The is_admin of this AccessKeyOutputV1.
        :rtype: bool
        """
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        """
        Sets the is_admin of this AccessKeyOutputV1.
        Is Admin Capable

        :param is_admin: The is_admin of this AccessKeyOutputV1.
        :type: bool
        """

        self._is_admin = is_admin

    @property
    def is_archived(self):
        """
        Gets the is_archived of this AccessKeyOutputV1.
        Whether item is archived

        :return: The is_archived of this AccessKeyOutputV1.
        :rtype: bool
        """
        return self._is_archived

    @is_archived.setter
    def is_archived(self, is_archived):
        """
        Sets the is_archived of this AccessKeyOutputV1.
        Whether item is archived

        :param is_archived: The is_archived of this AccessKeyOutputV1.
        :type: bool
        """

        self._is_archived = is_archived

    @property
    def is_redacted(self):
        """
        Gets the is_redacted of this AccessKeyOutputV1.
        Whether item is redacted

        :return: The is_redacted of this AccessKeyOutputV1.
        :rtype: bool
        """
        return self._is_redacted

    @is_redacted.setter
    def is_redacted(self, is_redacted):
        """
        Sets the is_redacted of this AccessKeyOutputV1.
        Whether item is redacted

        :param is_redacted: The is_redacted of this AccessKeyOutputV1.
        :type: bool
        """

        self._is_redacted = is_redacted

    @property
    def key_id(self):
        """
        Gets the key_id of this AccessKeyOutputV1.
        The ID of the key

        :return: The key_id of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """
        Sets the key_id of this AccessKeyOutputV1.
        The ID of the key

        :param key_id: The key_id of this AccessKeyOutputV1.
        :type: str
        """
        if key_id is None:
            raise ValueError("Invalid value for `key_id`, must not be `None`")

        self._key_id = key_id

    @property
    def last_used(self):
        """
        Gets the last_used of this AccessKeyOutputV1.
        The date this API Key was last used

        :return: The last_used of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._last_used

    @last_used.setter
    def last_used(self, last_used):
        """
        Sets the last_used of this AccessKeyOutputV1.
        The date this API Key was last used

        :param last_used: The last_used of this AccessKeyOutputV1.
        :type: str
        """

        self._last_used = last_used

    @property
    def name(self):
        """
        Gets the name of this AccessKeyOutputV1.
        The human readable name

        :return: The name of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AccessKeyOutputV1.
        The human readable name

        :param name: The name of this AccessKeyOutputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def password(self):
        """
        Gets the password of this AccessKeyOutputV1.
        The password portion of this API Key

        :return: The password of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password of this AccessKeyOutputV1.
        The password portion of this API Key

        :param password: The password of this AccessKeyOutputV1.
        :type: str
        """

        self._password = password

    @property
    def status_message(self):
        """
        Gets the status_message of this AccessKeyOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :return: The status_message of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this AccessKeyOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :param status_message: The status_message of this AccessKeyOutputV1.
        :type: str
        """

        self._status_message = status_message

    @property
    def type(self):
        """
        Gets the type of this AccessKeyOutputV1.
        The type of the item

        :return: The type of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this AccessKeyOutputV1.
        The type of the item

        :param type: The type of this AccessKeyOutputV1.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")

        self._type = type

    @property
    def user_id(self):
        """
        Gets the user_id of this AccessKeyOutputV1.
        The ID of the user this API Key maps to

        :return: The user_id of this AccessKeyOutputV1.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this AccessKeyOutputV1.
        The ID of the user this API Key maps to

        :param user_id: The user_id of this AccessKeyOutputV1.
        :type: str
        """

        self._user_id = user_id

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
        if not isinstance(other, AccessKeyOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

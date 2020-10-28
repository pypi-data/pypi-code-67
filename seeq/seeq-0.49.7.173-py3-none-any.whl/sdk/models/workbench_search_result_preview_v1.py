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


class WorkbenchSearchResultPreviewV1(object):
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
        'ancestors': 'list[ItemPreviewV1]',
        'created_at': 'str',
        'data': 'str',
        'description': 'str',
        'effective_permissions': 'PermissionsV1',
        'headline': 'str',
        'id': 'str',
        'is_pinned': 'bool',
        'name': 'str',
        'owner': 'IdentityPreviewV1',
        'parent_folder_id': 'str',
        'renderer': 'IdentityPreviewV1',
        'type': 'str',
        'updated_at': 'str'
    }

    attribute_map = {
        'ancestors': 'ancestors',
        'created_at': 'createdAt',
        'data': 'data',
        'description': 'description',
        'effective_permissions': 'effectivePermissions',
        'headline': 'headline',
        'id': 'id',
        'is_pinned': 'isPinned',
        'name': 'name',
        'owner': 'owner',
        'parent_folder_id': 'parentFolderId',
        'renderer': 'renderer',
        'type': 'type',
        'updated_at': 'updatedAt'
    }

    def __init__(self, ancestors=None, created_at=None, data=None, description=None, effective_permissions=None, headline=None, id=None, is_pinned=False, name=None, owner=None, parent_folder_id=None, renderer=None, type=None, updated_at=None):
        """
        WorkbenchSearchResultPreviewV1 - a model defined in Swagger
        """

        self._ancestors = None
        self._created_at = None
        self._data = None
        self._description = None
        self._effective_permissions = None
        self._headline = None
        self._id = None
        self._is_pinned = None
        self._name = None
        self._owner = None
        self._parent_folder_id = None
        self._renderer = None
        self._type = None
        self._updated_at = None

        if ancestors is not None:
          self.ancestors = ancestors
        if created_at is not None:
          self.created_at = created_at
        if data is not None:
          self.data = data
        if description is not None:
          self.description = description
        if effective_permissions is not None:
          self.effective_permissions = effective_permissions
        if headline is not None:
          self.headline = headline
        if id is not None:
          self.id = id
        if is_pinned is not None:
          self.is_pinned = is_pinned
        if name is not None:
          self.name = name
        if owner is not None:
          self.owner = owner
        if parent_folder_id is not None:
          self.parent_folder_id = parent_folder_id
        if renderer is not None:
          self.renderer = renderer
        if type is not None:
          self.type = type
        if updated_at is not None:
          self.updated_at = updated_at

    @property
    def ancestors(self):
        """
        Gets the ancestors of this WorkbenchSearchResultPreviewV1.
        The list of the item's folder ancestors, starting at the topmost folder to which the user has access

        :return: The ancestors of this WorkbenchSearchResultPreviewV1.
        :rtype: list[ItemPreviewV1]
        """
        return self._ancestors

    @ancestors.setter
    def ancestors(self, ancestors):
        """
        Sets the ancestors of this WorkbenchSearchResultPreviewV1.
        The list of the item's folder ancestors, starting at the topmost folder to which the user has access

        :param ancestors: The ancestors of this WorkbenchSearchResultPreviewV1.
        :type: list[ItemPreviewV1]
        """

        self._ancestors = ancestors

    @property
    def created_at(self):
        """
        Gets the created_at of this WorkbenchSearchResultPreviewV1.
        The ISO 8601 date of when the item was created (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :return: The created_at of this WorkbenchSearchResultPreviewV1.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this WorkbenchSearchResultPreviewV1.
        The ISO 8601 date of when the item was created (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :param created_at: The created_at of this WorkbenchSearchResultPreviewV1.
        :type: str
        """

        self._created_at = created_at

    @property
    def data(self):
        """
        Gets the data of this WorkbenchSearchResultPreviewV1.

        :return: The data of this WorkbenchSearchResultPreviewV1.
        :rtype: str
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this WorkbenchSearchResultPreviewV1.

        :param data: The data of this WorkbenchSearchResultPreviewV1.
        :type: str
        """

        self._data = data

    @property
    def description(self):
        """
        Gets the description of this WorkbenchSearchResultPreviewV1.

        :return: The description of this WorkbenchSearchResultPreviewV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this WorkbenchSearchResultPreviewV1.

        :param description: The description of this WorkbenchSearchResultPreviewV1.
        :type: str
        """

        self._description = description

    @property
    def effective_permissions(self):
        """
        Gets the effective_permissions of this WorkbenchSearchResultPreviewV1.
        The permissions the current user has to the item.

        :return: The effective_permissions of this WorkbenchSearchResultPreviewV1.
        :rtype: PermissionsV1
        """
        return self._effective_permissions

    @effective_permissions.setter
    def effective_permissions(self, effective_permissions):
        """
        Sets the effective_permissions of this WorkbenchSearchResultPreviewV1.
        The permissions the current user has to the item.

        :param effective_permissions: The effective_permissions of this WorkbenchSearchResultPreviewV1.
        :type: PermissionsV1
        """

        self._effective_permissions = effective_permissions

    @property
    def headline(self):
        """
        Gets the headline of this WorkbenchSearchResultPreviewV1.

        :return: The headline of this WorkbenchSearchResultPreviewV1.
        :rtype: str
        """
        return self._headline

    @headline.setter
    def headline(self, headline):
        """
        Sets the headline of this WorkbenchSearchResultPreviewV1.

        :param headline: The headline of this WorkbenchSearchResultPreviewV1.
        :type: str
        """

        self._headline = headline

    @property
    def id(self):
        """
        Gets the id of this WorkbenchSearchResultPreviewV1.

        :return: The id of this WorkbenchSearchResultPreviewV1.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WorkbenchSearchResultPreviewV1.

        :param id: The id of this WorkbenchSearchResultPreviewV1.
        :type: str
        """

        self._id = id

    @property
    def is_pinned(self):
        """
        Gets the is_pinned of this WorkbenchSearchResultPreviewV1.
        Flag indicating whether this item has been marked as a favorite by the current user

        :return: The is_pinned of this WorkbenchSearchResultPreviewV1.
        :rtype: bool
        """
        return self._is_pinned

    @is_pinned.setter
    def is_pinned(self, is_pinned):
        """
        Sets the is_pinned of this WorkbenchSearchResultPreviewV1.
        Flag indicating whether this item has been marked as a favorite by the current user

        :param is_pinned: The is_pinned of this WorkbenchSearchResultPreviewV1.
        :type: bool
        """

        self._is_pinned = is_pinned

    @property
    def name(self):
        """
        Gets the name of this WorkbenchSearchResultPreviewV1.

        :return: The name of this WorkbenchSearchResultPreviewV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this WorkbenchSearchResultPreviewV1.

        :param name: The name of this WorkbenchSearchResultPreviewV1.
        :type: str
        """

        self._name = name

    @property
    def owner(self):
        """
        Gets the owner of this WorkbenchSearchResultPreviewV1.
        The owner of this item

        :return: The owner of this WorkbenchSearchResultPreviewV1.
        :rtype: IdentityPreviewV1
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        Sets the owner of this WorkbenchSearchResultPreviewV1.
        The owner of this item

        :param owner: The owner of this WorkbenchSearchResultPreviewV1.
        :type: IdentityPreviewV1
        """

        self._owner = owner

    @property
    def parent_folder_id(self):
        """
        Gets the parent_folder_id of this WorkbenchSearchResultPreviewV1.
        The ID of the folder this item belongs to

        :return: The parent_folder_id of this WorkbenchSearchResultPreviewV1.
        :rtype: str
        """
        return self._parent_folder_id

    @parent_folder_id.setter
    def parent_folder_id(self, parent_folder_id):
        """
        Sets the parent_folder_id of this WorkbenchSearchResultPreviewV1.
        The ID of the folder this item belongs to

        :param parent_folder_id: The parent_folder_id of this WorkbenchSearchResultPreviewV1.
        :type: str
        """

        self._parent_folder_id = parent_folder_id

    @property
    def renderer(self):
        """
        Gets the renderer of this WorkbenchSearchResultPreviewV1.
        The renderer of this item, if any

        :return: The renderer of this WorkbenchSearchResultPreviewV1.
        :rtype: IdentityPreviewV1
        """
        return self._renderer

    @renderer.setter
    def renderer(self, renderer):
        """
        Sets the renderer of this WorkbenchSearchResultPreviewV1.
        The renderer of this item, if any

        :param renderer: The renderer of this WorkbenchSearchResultPreviewV1.
        :type: IdentityPreviewV1
        """

        self._renderer = renderer

    @property
    def type(self):
        """
        Gets the type of this WorkbenchSearchResultPreviewV1.

        :return: The type of this WorkbenchSearchResultPreviewV1.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this WorkbenchSearchResultPreviewV1.

        :param type: The type of this WorkbenchSearchResultPreviewV1.
        :type: str
        """

        self._type = type

    @property
    def updated_at(self):
        """
        Gets the updated_at of this WorkbenchSearchResultPreviewV1.
        The ISO 8601 date of when the item was last updated (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :return: The updated_at of this WorkbenchSearchResultPreviewV1.
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this WorkbenchSearchResultPreviewV1.
        The ISO 8601 date of when the item was last updated (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :param updated_at: The updated_at of this WorkbenchSearchResultPreviewV1.
        :type: str
        """

        self._updated_at = updated_at

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
        if not isinstance(other, WorkbenchSearchResultPreviewV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

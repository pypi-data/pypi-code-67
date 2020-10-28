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


class AceOutputV1(object):
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
        'href': 'str',
        'id': 'str',
        'identity': 'IdentityPreviewV1',
        'origin': 'ItemPreviewV1',
        'permissions': 'PermissionsV1',
        'role': 'str'
    }

    attribute_map = {
        'href': 'href',
        'id': 'id',
        'identity': 'identity',
        'origin': 'origin',
        'permissions': 'permissions',
        'role': 'role'
    }

    def __init__(self, href=None, id=None, identity=None, origin=None, permissions=None, role=None):
        """
        AceOutputV1 - a model defined in Swagger
        """

        self._href = None
        self._id = None
        self._identity = None
        self._origin = None
        self._permissions = None
        self._role = None

        if href is not None:
          self.href = href
        if id is not None:
          self.id = id
        if identity is not None:
          self.identity = identity
        if origin is not None:
          self.origin = origin
        if permissions is not None:
          self.permissions = permissions
        if role is not None:
          self.role = role

    @property
    def href(self):
        """
        Gets the href of this AceOutputV1.
        The href that can be used to interact with the item

        :return: The href of this AceOutputV1.
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """
        Sets the href of this AceOutputV1.
        The href that can be used to interact with the item

        :param href: The href of this AceOutputV1.
        :type: str
        """
        if href is None:
            raise ValueError("Invalid value for `href`, must not be `None`")

        self._href = href

    @property
    def id(self):
        """
        Gets the id of this AceOutputV1.
        The ID that can be used to interact with the item

        :return: The id of this AceOutputV1.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AceOutputV1.
        The ID that can be used to interact with the item

        :param id: The id of this AceOutputV1.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def identity(self):
        """
        Gets the identity of this AceOutputV1.
        Get the identity that the ACE restricts access for

        :return: The identity of this AceOutputV1.
        :rtype: IdentityPreviewV1
        """
        return self._identity

    @identity.setter
    def identity(self, identity):
        """
        Sets the identity of this AceOutputV1.
        Get the identity that the ACE restricts access for

        :param identity: The identity of this AceOutputV1.
        :type: IdentityPreviewV1
        """

        self._identity = identity

    @property
    def origin(self):
        """
        Gets the origin of this AceOutputV1.
        Get the origin of this ACE if it's inherited. If the ACE is set on the item itself, origin is null.

        :return: The origin of this AceOutputV1.
        :rtype: ItemPreviewV1
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """
        Sets the origin of this AceOutputV1.
        Get the origin of this ACE if it's inherited. If the ACE is set on the item itself, origin is null.

        :param origin: The origin of this AceOutputV1.
        :type: ItemPreviewV1
        """

        self._origin = origin

    @property
    def permissions(self):
        """
        Gets the permissions of this AceOutputV1.
        Get the permissions of this ACE

        :return: The permissions of this AceOutputV1.
        :rtype: PermissionsV1
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """
        Sets the permissions of this AceOutputV1.
        Get the permissions of this ACE

        :param permissions: The permissions of this AceOutputV1.
        :type: PermissionsV1
        """

        self._permissions = permissions

    @property
    def role(self):
        """
        Gets the role of this AceOutputV1.
        The role of a system managed ACE

        :return: The role of this AceOutputV1.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """
        Sets the role of this AceOutputV1.
        The role of a system managed ACE

        :param role: The role of this AceOutputV1.
        :type: str
        """

        self._role = role

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
        if not isinstance(other, AceOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

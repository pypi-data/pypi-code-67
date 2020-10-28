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


class PutScalarsInputV1(object):
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
        'datasource_class': 'str',
        'datasource_id': 'str',
        'scalars': 'list[ScalarInputV1]'
    }

    attribute_map = {
        'datasource_class': 'datasourceClass',
        'datasource_id': 'datasourceId',
        'scalars': 'scalars'
    }

    def __init__(self, datasource_class=None, datasource_id=None, scalars=None):
        """
        PutScalarsInputV1 - a model defined in Swagger
        """

        self._datasource_class = None
        self._datasource_id = None
        self._scalars = None

        if datasource_class is not None:
          self.datasource_class = datasource_class
        if datasource_id is not None:
          self.datasource_id = datasource_id
        if scalars is not None:
          self.scalars = scalars

    @property
    def datasource_class(self):
        """
        Gets the datasource_class of this PutScalarsInputV1.
        Along with the Datasource ID, the Datasource Class uniquely identifies a datasource. For example, a datasource may be a particular instance of an OSIsoft PI historian.

        :return: The datasource_class of this PutScalarsInputV1.
        :rtype: str
        """
        return self._datasource_class

    @datasource_class.setter
    def datasource_class(self, datasource_class):
        """
        Sets the datasource_class of this PutScalarsInputV1.
        Along with the Datasource ID, the Datasource Class uniquely identifies a datasource. For example, a datasource may be a particular instance of an OSIsoft PI historian.

        :param datasource_class: The datasource_class of this PutScalarsInputV1.
        :type: str
        """
        if datasource_class is None:
            raise ValueError("Invalid value for `datasource_class`, must not be `None`")

        self._datasource_class = datasource_class

    @property
    def datasource_id(self):
        """
        Gets the datasource_id of this PutScalarsInputV1.
        Along with the Datasource Class, the Datasource ID uniquely identifies a datasource. For example, a datasource may be a particular instance of an OSIsoft PI historian.

        :return: The datasource_id of this PutScalarsInputV1.
        :rtype: str
        """
        return self._datasource_id

    @datasource_id.setter
    def datasource_id(self, datasource_id):
        """
        Sets the datasource_id of this PutScalarsInputV1.
        Along with the Datasource Class, the Datasource ID uniquely identifies a datasource. For example, a datasource may be a particular instance of an OSIsoft PI historian.

        :param datasource_id: The datasource_id of this PutScalarsInputV1.
        :type: str
        """
        if datasource_id is None:
            raise ValueError("Invalid value for `datasource_id`, must not be `None`")

        self._datasource_id = datasource_id

    @property
    def scalars(self):
        """
        Gets the scalars of this PutScalarsInputV1.
        A list of scalars to create or update

        :return: The scalars of this PutScalarsInputV1.
        :rtype: list[ScalarInputV1]
        """
        return self._scalars

    @scalars.setter
    def scalars(self, scalars):
        """
        Sets the scalars of this PutScalarsInputV1.
        A list of scalars to create or update

        :param scalars: The scalars of this PutScalarsInputV1.
        :type: list[ScalarInputV1]
        """
        if scalars is None:
            raise ValueError("Invalid value for `scalars`, must not be `None`")

        self._scalars = scalars

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
        if not isinstance(other, PutScalarsInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

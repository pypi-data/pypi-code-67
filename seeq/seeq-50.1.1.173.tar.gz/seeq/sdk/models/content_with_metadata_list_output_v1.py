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


class ContentWithMetadataListOutputV1(object):
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
        'content_items': 'list[ContentWithMetadataOutputV1]',
        'date_ranges': 'list[DateRangeOutputV1]'
    }

    attribute_map = {
        'content_items': 'contentItems',
        'date_ranges': 'dateRanges'
    }

    def __init__(self, content_items=None, date_ranges=None):
        """
        ContentWithMetadataListOutputV1 - a model defined in Swagger
        """

        self._content_items = None
        self._date_ranges = None

        if content_items is not None:
          self.content_items = content_items
        if date_ranges is not None:
          self.date_ranges = date_ranges

    @property
    def content_items(self):
        """
        Gets the content_items of this ContentWithMetadataListOutputV1.
        A list of content items

        :return: The content_items of this ContentWithMetadataListOutputV1.
        :rtype: list[ContentWithMetadataOutputV1]
        """
        return self._content_items

    @content_items.setter
    def content_items(self, content_items):
        """
        Sets the content_items of this ContentWithMetadataListOutputV1.
        A list of content items

        :param content_items: The content_items of this ContentWithMetadataListOutputV1.
        :type: list[ContentWithMetadataOutputV1]
        """

        self._content_items = content_items

    @property
    def date_ranges(self):
        """
        Gets the date_ranges of this ContentWithMetadataListOutputV1.
        A list of date ranges

        :return: The date_ranges of this ContentWithMetadataListOutputV1.
        :rtype: list[DateRangeOutputV1]
        """
        return self._date_ranges

    @date_ranges.setter
    def date_ranges(self, date_ranges):
        """
        Sets the date_ranges of this ContentWithMetadataListOutputV1.
        A list of date ranges

        :param date_ranges: The date_ranges of this ContentWithMetadataListOutputV1.
        :type: list[DateRangeOutputV1]
        """

        self._date_ranges = date_ranges

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
        if not isinstance(other, ContentWithMetadataListOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

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


class FormulaDocInputV1(object):
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
        'description': 'str',
        'examples': 'FormulaDocExampleListInputV1',
        'search_keywords': 'FormulaDocKeywordListInputV1',
        'title': 'str'
    }

    attribute_map = {
        'description': 'description',
        'examples': 'examples',
        'search_keywords': 'searchKeywords',
        'title': 'title'
    }

    def __init__(self, description=None, examples=None, search_keywords=None, title=None):
        """
        FormulaDocInputV1 - a model defined in Swagger
        """

        self._description = None
        self._examples = None
        self._search_keywords = None
        self._title = None

        if description is not None:
          self.description = description
        if examples is not None:
          self.examples = examples
        if search_keywords is not None:
          self.search_keywords = search_keywords
        if title is not None:
          self.title = title

    @property
    def description(self):
        """
        Gets the description of this FormulaDocInputV1.
        The body of this FormulaDoc.

        :return: The description of this FormulaDocInputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FormulaDocInputV1.
        The body of this FormulaDoc.

        :param description: The description of this FormulaDocInputV1.
        :type: str
        """

        self._description = description

    @property
    def examples(self):
        """
        Gets the examples of this FormulaDocInputV1.
        Formula examples demonstrating the functions in this document.

        :return: The examples of this FormulaDocInputV1.
        :rtype: FormulaDocExampleListInputV1
        """
        return self._examples

    @examples.setter
    def examples(self, examples):
        """
        Sets the examples of this FormulaDocInputV1.
        Formula examples demonstrating the functions in this document.

        :param examples: The examples of this FormulaDocInputV1.
        :type: FormulaDocExampleListInputV1
        """

        self._examples = examples

    @property
    def search_keywords(self):
        """
        Gets the search_keywords of this FormulaDocInputV1.
        Search keywords to allow this document to be found more easily.

        :return: The search_keywords of this FormulaDocInputV1.
        :rtype: FormulaDocKeywordListInputV1
        """
        return self._search_keywords

    @search_keywords.setter
    def search_keywords(self, search_keywords):
        """
        Sets the search_keywords of this FormulaDocInputV1.
        Search keywords to allow this document to be found more easily.

        :param search_keywords: The search_keywords of this FormulaDocInputV1.
        :type: FormulaDocKeywordListInputV1
        """

        self._search_keywords = search_keywords

    @property
    def title(self):
        """
        Gets the title of this FormulaDocInputV1.
        The title of the page. This may only be set on index pages.

        :return: The title of this FormulaDocInputV1.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this FormulaDocInputV1.
        The title of the page. This may only be set on index pages.

        :param title: The title of this FormulaDocInputV1.
        :type: str
        """

        self._title = title

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
        if not isinstance(other, FormulaDocInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

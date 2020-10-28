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


class FormulaDocSummaryOutputV1(object):
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
        'documentation_href': 'str',
        'excel_synonyms': 'list[str]',
        'fluent': 'bool',
        'keywords': 'list[str]',
        'name': 'str',
        'short_description': 'str'
    }

    attribute_map = {
        'description': 'description',
        'documentation_href': 'documentationHref',
        'excel_synonyms': 'excelSynonyms',
        'fluent': 'fluent',
        'keywords': 'keywords',
        'name': 'name',
        'short_description': 'shortDescription'
    }

    def __init__(self, description=None, documentation_href=None, excel_synonyms=None, fluent=False, keywords=None, name=None, short_description=None):
        """
        FormulaDocSummaryOutputV1 - a model defined in Swagger
        """

        self._description = None
        self._documentation_href = None
        self._excel_synonyms = None
        self._fluent = None
        self._keywords = None
        self._name = None
        self._short_description = None

        if description is not None:
          self.description = description
        if documentation_href is not None:
          self.documentation_href = documentation_href
        if excel_synonyms is not None:
          self.excel_synonyms = excel_synonyms
        if fluent is not None:
          self.fluent = fluent
        if keywords is not None:
          self.keywords = keywords
        if name is not None:
          self.name = name
        if short_description is not None:
          self.short_description = short_description

    @property
    def description(self):
        """
        Gets the description of this FormulaDocSummaryOutputV1.
        A detailed description of the page

        :return: The description of this FormulaDocSummaryOutputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FormulaDocSummaryOutputV1.
        A detailed description of the page

        :param description: The description of this FormulaDocSummaryOutputV1.
        :type: str
        """

        self._description = description

    @property
    def documentation_href(self):
        """
        Gets the documentation_href of this FormulaDocSummaryOutputV1.
        The href to the documentation

        :return: The documentation_href of this FormulaDocSummaryOutputV1.
        :rtype: str
        """
        return self._documentation_href

    @documentation_href.setter
    def documentation_href(self, documentation_href):
        """
        Sets the documentation_href of this FormulaDocSummaryOutputV1.
        The href to the documentation

        :param documentation_href: The documentation_href of this FormulaDocSummaryOutputV1.
        :type: str
        """

        self._documentation_href = documentation_href

    @property
    def excel_synonyms(self):
        """
        Gets the excel_synonyms of this FormulaDocSummaryOutputV1.
        Search synonyms for this document, generally corresponding to an excel function

        :return: The excel_synonyms of this FormulaDocSummaryOutputV1.
        :rtype: list[str]
        """
        return self._excel_synonyms

    @excel_synonyms.setter
    def excel_synonyms(self, excel_synonyms):
        """
        Sets the excel_synonyms of this FormulaDocSummaryOutputV1.
        Search synonyms for this document, generally corresponding to an excel function

        :param excel_synonyms: The excel_synonyms of this FormulaDocSummaryOutputV1.
        :type: list[str]
        """

        self._excel_synonyms = excel_synonyms

    @property
    def fluent(self):
        """
        Gets the fluent of this FormulaDocSummaryOutputV1.

        :return: The fluent of this FormulaDocSummaryOutputV1.
        :rtype: bool
        """
        return self._fluent

    @fluent.setter
    def fluent(self, fluent):
        """
        Sets the fluent of this FormulaDocSummaryOutputV1.

        :param fluent: The fluent of this FormulaDocSummaryOutputV1.
        :type: bool
        """

        self._fluent = fluent

    @property
    def keywords(self):
        """
        Gets the keywords of this FormulaDocSummaryOutputV1.
        Keywords of the documentation page

        :return: The keywords of this FormulaDocSummaryOutputV1.
        :rtype: list[str]
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        """
        Sets the keywords of this FormulaDocSummaryOutputV1.
        Keywords of the documentation page

        :param keywords: The keywords of this FormulaDocSummaryOutputV1.
        :type: list[str]
        """

        self._keywords = keywords

    @property
    def name(self):
        """
        Gets the name of this FormulaDocSummaryOutputV1.
        The identifier of the documentation

        :return: The name of this FormulaDocSummaryOutputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FormulaDocSummaryOutputV1.
        The identifier of the documentation

        :param name: The name of this FormulaDocSummaryOutputV1.
        :type: str
        """

        self._name = name

    @property
    def short_description(self):
        """
        Gets the short_description of this FormulaDocSummaryOutputV1.
        A short description of the page

        :return: The short_description of this FormulaDocSummaryOutputV1.
        :rtype: str
        """
        return self._short_description

    @short_description.setter
    def short_description(self, short_description):
        """
        Sets the short_description of this FormulaDocSummaryOutputV1.
        A short description of the page

        :param short_description: The short_description of this FormulaDocSummaryOutputV1.
        :type: str
        """

        self._short_description = short_description

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
        if not isinstance(other, FormulaDocSummaryOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

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


class FormulaUpgradeOutputV1(object):
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
        'after_formula': 'str',
        'before_formula': 'str',
        'changes': 'list[FormulaUpgradeChangeV1]'
    }

    attribute_map = {
        'after_formula': 'afterFormula',
        'before_formula': 'beforeFormula',
        'changes': 'changes'
    }

    def __init__(self, after_formula=None, before_formula=None, changes=None):
        """
        FormulaUpgradeOutputV1 - a model defined in Swagger
        """

        self._after_formula = None
        self._before_formula = None
        self._changes = None

        if after_formula is not None:
          self.after_formula = after_formula
        if before_formula is not None:
          self.before_formula = before_formula
        if changes is not None:
          self.changes = changes

    @property
    def after_formula(self):
        """
        Gets the after_formula of this FormulaUpgradeOutputV1.
        The resulting changed formula

        :return: The after_formula of this FormulaUpgradeOutputV1.
        :rtype: str
        """
        return self._after_formula

    @after_formula.setter
    def after_formula(self, after_formula):
        """
        Sets the after_formula of this FormulaUpgradeOutputV1.
        The resulting changed formula

        :param after_formula: The after_formula of this FormulaUpgradeOutputV1.
        :type: str
        """

        self._after_formula = after_formula

    @property
    def before_formula(self):
        """
        Gets the before_formula of this FormulaUpgradeOutputV1.
        The original input formula

        :return: The before_formula of this FormulaUpgradeOutputV1.
        :rtype: str
        """
        return self._before_formula

    @before_formula.setter
    def before_formula(self, before_formula):
        """
        Sets the before_formula of this FormulaUpgradeOutputV1.
        The original input formula

        :param before_formula: The before_formula of this FormulaUpgradeOutputV1.
        :type: str
        """

        self._before_formula = before_formula

    @property
    def changes(self):
        """
        Gets the changes of this FormulaUpgradeOutputV1.
        Details about the specific changes

        :return: The changes of this FormulaUpgradeOutputV1.
        :rtype: list[FormulaUpgradeChangeV1]
        """
        return self._changes

    @changes.setter
    def changes(self, changes):
        """
        Sets the changes of this FormulaUpgradeOutputV1.
        Details about the specific changes

        :param changes: The changes of this FormulaUpgradeOutputV1.
        :type: list[FormulaUpgradeChangeV1]
        """

        self._changes = changes

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
        if not isinstance(other, FormulaUpgradeOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

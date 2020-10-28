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


class FormulaRunOutputV1(object):
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
        'capsules': 'CapsulesOutputV1',
        'items': 'ItemPreviewListV1',
        'metadata': 'dict(str, str)',
        'regression_output': 'RegressionOutputV1',
        'return_type': 'str',
        'samples': 'SeriesSamplesOutputV1',
        'scalar': 'ScalarValueOutputV1',
        'status_message': 'str',
        'table': 'GenericTableOutputV1',
        'upgrade_details': 'FormulaUpgradeOutputV1',
        'warning_count': 'int',
        'warning_logs': 'list[FormulaLogV1]'
    }

    attribute_map = {
        'capsules': 'capsules',
        'items': 'items',
        'metadata': 'metadata',
        'regression_output': 'regressionOutput',
        'return_type': 'returnType',
        'samples': 'samples',
        'scalar': 'scalar',
        'status_message': 'statusMessage',
        'table': 'table',
        'upgrade_details': 'upgradeDetails',
        'warning_count': 'warningCount',
        'warning_logs': 'warningLogs'
    }

    def __init__(self, capsules=None, items=None, metadata=None, regression_output=None, return_type=None, samples=None, scalar=None, status_message=None, table=None, upgrade_details=None, warning_count=None, warning_logs=None):
        """
        FormulaRunOutputV1 - a model defined in Swagger
        """

        self._capsules = None
        self._items = None
        self._metadata = None
        self._regression_output = None
        self._return_type = None
        self._samples = None
        self._scalar = None
        self._status_message = None
        self._table = None
        self._upgrade_details = None
        self._warning_count = None
        self._warning_logs = None

        if capsules is not None:
          self.capsules = capsules
        if items is not None:
          self.items = items
        if metadata is not None:
          self.metadata = metadata
        if regression_output is not None:
          self.regression_output = regression_output
        if return_type is not None:
          self.return_type = return_type
        if samples is not None:
          self.samples = samples
        if scalar is not None:
          self.scalar = scalar
        if status_message is not None:
          self.status_message = status_message
        if table is not None:
          self.table = table
        if upgrade_details is not None:
          self.upgrade_details = upgrade_details
        if warning_count is not None:
          self.warning_count = warning_count
        if warning_logs is not None:
          self.warning_logs = warning_logs

    @property
    def capsules(self):
        """
        Gets the capsules of this FormulaRunOutputV1.
        Capsules from the formula result

        :return: The capsules of this FormulaRunOutputV1.
        :rtype: CapsulesOutputV1
        """
        return self._capsules

    @capsules.setter
    def capsules(self, capsules):
        """
        Sets the capsules of this FormulaRunOutputV1.
        Capsules from the formula result

        :param capsules: The capsules of this FormulaRunOutputV1.
        :type: CapsulesOutputV1
        """

        self._capsules = capsules

    @property
    def items(self):
        """
        Gets the items of this FormulaRunOutputV1.
        Items from the formula result

        :return: The items of this FormulaRunOutputV1.
        :rtype: ItemPreviewListV1
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this FormulaRunOutputV1.
        Items from the formula result

        :param items: The items of this FormulaRunOutputV1.
        :type: ItemPreviewListV1
        """

        self._items = items

    @property
    def metadata(self):
        """
        Gets the metadata of this FormulaRunOutputV1.
        Metadata describing the compiled formula's result

        :return: The metadata of this FormulaRunOutputV1.
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this FormulaRunOutputV1.
        Metadata describing the compiled formula's result

        :param metadata: The metadata of this FormulaRunOutputV1.
        :type: dict(str, str)
        """

        self._metadata = metadata

    @property
    def regression_output(self):
        """
        Gets the regression_output of this FormulaRunOutputV1.
        Regression output from the formula result. Note that the `table` will also contain values.

        :return: The regression_output of this FormulaRunOutputV1.
        :rtype: RegressionOutputV1
        """
        return self._regression_output

    @regression_output.setter
    def regression_output(self, regression_output):
        """
        Sets the regression_output of this FormulaRunOutputV1.
        Regression output from the formula result. Note that the `table` will also contain values.

        :param regression_output: The regression_output of this FormulaRunOutputV1.
        :type: RegressionOutputV1
        """

        self._regression_output = regression_output

    @property
    def return_type(self):
        """
        Gets the return_type of this FormulaRunOutputV1.
        The data type of the compiled formula's result

        :return: The return_type of this FormulaRunOutputV1.
        :rtype: str
        """
        return self._return_type

    @return_type.setter
    def return_type(self, return_type):
        """
        Sets the return_type of this FormulaRunOutputV1.
        The data type of the compiled formula's result

        :param return_type: The return_type of this FormulaRunOutputV1.
        :type: str
        """

        self._return_type = return_type

    @property
    def samples(self):
        """
        Gets the samples of this FormulaRunOutputV1.
        Samples from the formula result

        :return: The samples of this FormulaRunOutputV1.
        :rtype: SeriesSamplesOutputV1
        """
        return self._samples

    @samples.setter
    def samples(self, samples):
        """
        Sets the samples of this FormulaRunOutputV1.
        Samples from the formula result

        :param samples: The samples of this FormulaRunOutputV1.
        :type: SeriesSamplesOutputV1
        """

        self._samples = samples

    @property
    def scalar(self):
        """
        Gets the scalar of this FormulaRunOutputV1.
        Scalar from the formula result

        :return: The scalar of this FormulaRunOutputV1.
        :rtype: ScalarValueOutputV1
        """
        return self._scalar

    @scalar.setter
    def scalar(self, scalar):
        """
        Sets the scalar of this FormulaRunOutputV1.
        Scalar from the formula result

        :param scalar: The scalar of this FormulaRunOutputV1.
        :type: ScalarValueOutputV1
        """

        self._scalar = scalar

    @property
    def status_message(self):
        """
        Gets the status_message of this FormulaRunOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation. Null if the status message has not been set.

        :return: The status_message of this FormulaRunOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this FormulaRunOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation. Null if the status message has not been set.

        :param status_message: The status_message of this FormulaRunOutputV1.
        :type: str
        """

        self._status_message = status_message

    @property
    def table(self):
        """
        Gets the table of this FormulaRunOutputV1.
        Table from the formula result

        :return: The table of this FormulaRunOutputV1.
        :rtype: GenericTableOutputV1
        """
        return self._table

    @table.setter
    def table(self, table):
        """
        Sets the table of this FormulaRunOutputV1.
        Table from the formula result

        :param table: The table of this FormulaRunOutputV1.
        :type: GenericTableOutputV1
        """

        self._table = table

    @property
    def upgrade_details(self):
        """
        Gets the upgrade_details of this FormulaRunOutputV1.
        Contains upgrade information if the formula contains legacy syntax that was automatically updated

        :return: The upgrade_details of this FormulaRunOutputV1.
        :rtype: FormulaUpgradeOutputV1
        """
        return self._upgrade_details

    @upgrade_details.setter
    def upgrade_details(self, upgrade_details):
        """
        Sets the upgrade_details of this FormulaRunOutputV1.
        Contains upgrade information if the formula contains legacy syntax that was automatically updated

        :param upgrade_details: The upgrade_details of this FormulaRunOutputV1.
        :type: FormulaUpgradeOutputV1
        """

        self._upgrade_details = upgrade_details

    @property
    def warning_count(self):
        """
        Gets the warning_count of this FormulaRunOutputV1.
        The total number of warnings that have occurred

        :return: The warning_count of this FormulaRunOutputV1.
        :rtype: int
        """
        return self._warning_count

    @warning_count.setter
    def warning_count(self, warning_count):
        """
        Sets the warning_count of this FormulaRunOutputV1.
        The total number of warnings that have occurred

        :param warning_count: The warning_count of this FormulaRunOutputV1.
        :type: int
        """

        self._warning_count = warning_count

    @property
    def warning_logs(self):
        """
        Gets the warning_logs of this FormulaRunOutputV1.
        The Formula warning logs, which includes the text, line number, and column number where the warning occurred in addition to the warning details

        :return: The warning_logs of this FormulaRunOutputV1.
        :rtype: list[FormulaLogV1]
        """
        return self._warning_logs

    @warning_logs.setter
    def warning_logs(self, warning_logs):
        """
        Sets the warning_logs of this FormulaRunOutputV1.
        The Formula warning logs, which includes the text, line number, and column number where the warning occurred in addition to the warning details

        :param warning_logs: The warning_logs of this FormulaRunOutputV1.
        :type: list[FormulaLogV1]
        """

        self._warning_logs = warning_logs

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
        if not isinstance(other, FormulaRunOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

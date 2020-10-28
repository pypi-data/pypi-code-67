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


class ContentInputV1(object):
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
        'archived': 'bool',
        'date_range_id': 'str',
        'description': 'str',
        'height': 'int',
        'name': 'str',
        'report_id': 'str',
        'scale': 'float',
        'selector': 'str',
        'summary_type': 'str',
        'summary_value': 'str',
        'timezone': 'str',
        'width': 'int',
        'worksheet_id': 'str',
        'workstep_id': 'str'
    }

    attribute_map = {
        'archived': 'archived',
        'date_range_id': 'dateRangeId',
        'description': 'description',
        'height': 'height',
        'name': 'name',
        'report_id': 'reportId',
        'scale': 'scale',
        'selector': 'selector',
        'summary_type': 'summaryType',
        'summary_value': 'summaryValue',
        'timezone': 'timezone',
        'width': 'width',
        'worksheet_id': 'worksheetId',
        'workstep_id': 'workstepId'
    }

    def __init__(self, archived=False, date_range_id=None, description=None, height=None, name=None, report_id=None, scale=None, selector=None, summary_type=None, summary_value=None, timezone=None, width=None, worksheet_id=None, workstep_id=None):
        """
        ContentInputV1 - a model defined in Swagger
        """

        self._archived = None
        self._date_range_id = None
        self._description = None
        self._height = None
        self._name = None
        self._report_id = None
        self._scale = None
        self._selector = None
        self._summary_type = None
        self._summary_value = None
        self._timezone = None
        self._width = None
        self._worksheet_id = None
        self._workstep_id = None

        if archived is not None:
          self.archived = archived
        if date_range_id is not None:
          self.date_range_id = date_range_id
        if description is not None:
          self.description = description
        if height is not None:
          self.height = height
        if name is not None:
          self.name = name
        if report_id is not None:
          self.report_id = report_id
        if scale is not None:
          self.scale = scale
        if selector is not None:
          self.selector = selector
        if summary_type is not None:
          self.summary_type = summary_type
        if summary_value is not None:
          self.summary_value = summary_value
        if timezone is not None:
          self.timezone = timezone
        if width is not None:
          self.width = width
        if worksheet_id is not None:
          self.worksheet_id = worksheet_id
        if workstep_id is not None:
          self.workstep_id = workstep_id

    @property
    def archived(self):
        """
        Gets the archived of this ContentInputV1.
        Whether the content should be archived

        :return: The archived of this ContentInputV1.
        :rtype: bool
        """
        return self._archived

    @archived.setter
    def archived(self, archived):
        """
        Sets the archived of this ContentInputV1.
        Whether the content should be archived

        :param archived: The archived of this ContentInputV1.
        :type: bool
        """

        self._archived = archived

    @property
    def date_range_id(self):
        """
        Gets the date_range_id of this ContentInputV1.
        The content's date range

        :return: The date_range_id of this ContentInputV1.
        :rtype: str
        """
        return self._date_range_id

    @date_range_id.setter
    def date_range_id(self, date_range_id):
        """
        Sets the date_range_id of this ContentInputV1.
        The content's date range

        :param date_range_id: The date_range_id of this ContentInputV1.
        :type: str
        """

        self._date_range_id = date_range_id

    @property
    def description(self):
        """
        Gets the description of this ContentInputV1.
        The content's description

        :return: The description of this ContentInputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ContentInputV1.
        The content's description

        :param description: The description of this ContentInputV1.
        :type: str
        """

        self._description = description

    @property
    def height(self):
        """
        Gets the height of this ContentInputV1.
        The content's desired height

        :return: The height of this ContentInputV1.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """
        Sets the height of this ContentInputV1.
        The content's desired height

        :param height: The height of this ContentInputV1.
        :type: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")

        self._height = height

    @property
    def name(self):
        """
        Gets the name of this ContentInputV1.
        The content's name

        :return: The name of this ContentInputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ContentInputV1.
        The content's name

        :param name: The name of this ContentInputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def report_id(self):
        """
        Gets the report_id of this ContentInputV1.
        The content's report

        :return: The report_id of this ContentInputV1.
        :rtype: str
        """
        return self._report_id

    @report_id.setter
    def report_id(self, report_id):
        """
        Sets the report_id of this ContentInputV1.
        The content's report

        :param report_id: The report_id of this ContentInputV1.
        :type: str
        """

        self._report_id = report_id

    @property
    def scale(self):
        """
        Gets the scale of this ContentInputV1.
        The content's desired scale. A value greater than 1 will increase the size of elements within the screenshot. A value less than 1 will shrink the size of elements within the screenshot.

        :return: The scale of this ContentInputV1.
        :rtype: float
        """
        return self._scale

    @scale.setter
    def scale(self, scale):
        """
        Sets the scale of this ContentInputV1.
        The content's desired scale. A value greater than 1 will increase the size of elements within the screenshot. A value less than 1 will shrink the size of elements within the screenshot.

        :param scale: The scale of this ContentInputV1.
        :type: float
        """

        self._scale = scale

    @property
    def selector(self):
        """
        Gets the selector of this ContentInputV1.
        The content's desired selector

        :return: The selector of this ContentInputV1.
        :rtype: str
        """
        return self._selector

    @selector.setter
    def selector(self, selector):
        """
        Sets the selector of this ContentInputV1.
        The content's desired selector

        :param selector: The selector of this ContentInputV1.
        :type: str
        """

        self._selector = selector

    @property
    def summary_type(self):
        """
        Gets the summary_type of this ContentInputV1.
        The summary type for this screenshot if a summary is being applied. One of DISCRETE, NONE

        :return: The summary_type of this ContentInputV1.
        :rtype: str
        """
        return self._summary_type

    @summary_type.setter
    def summary_type(self, summary_type):
        """
        Sets the summary_type of this ContentInputV1.
        The summary type for this screenshot if a summary is being applied. One of DISCRETE, NONE

        :param summary_type: The summary_type of this ContentInputV1.
        :type: str
        """
        allowed_values = ["DISCRETE", "NONE"]
        if summary_type not in allowed_values:
            raise ValueError(
                "Invalid value for `summary_type` ({0}), must be one of {1}"
                .format(summary_type, allowed_values)
            )

        self._summary_type = summary_type

    @property
    def summary_value(self):
        """
        Gets the summary_value of this ContentInputV1.
        The value for the given summary type. If discrete, a time + unit pairing (1min, 2days). If auto, a fixed value (1-10).

        :return: The summary_value of this ContentInputV1.
        :rtype: str
        """
        return self._summary_value

    @summary_value.setter
    def summary_value(self, summary_value):
        """
        Sets the summary_value of this ContentInputV1.
        The value for the given summary type. If discrete, a time + unit pairing (1min, 2days). If auto, a fixed value (1-10).

        :param summary_value: The summary_value of this ContentInputV1.
        :type: str
        """

        self._summary_value = summary_value

    @property
    def timezone(self):
        """
        Gets the timezone of this ContentInputV1.
        The content's desired timezone

        :return: The timezone of this ContentInputV1.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """
        Sets the timezone of this ContentInputV1.
        The content's desired timezone

        :param timezone: The timezone of this ContentInputV1.
        :type: str
        """

        self._timezone = timezone

    @property
    def width(self):
        """
        Gets the width of this ContentInputV1.
        The content's desired width

        :return: The width of this ContentInputV1.
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """
        Sets the width of this ContentInputV1.
        The content's desired width

        :param width: The width of this ContentInputV1.
        :type: int
        """
        if width is None:
            raise ValueError("Invalid value for `width`, must not be `None`")

        self._width = width

    @property
    def worksheet_id(self):
        """
        Gets the worksheet_id of this ContentInputV1.
        The content's source worksheet

        :return: The worksheet_id of this ContentInputV1.
        :rtype: str
        """
        return self._worksheet_id

    @worksheet_id.setter
    def worksheet_id(self, worksheet_id):
        """
        Sets the worksheet_id of this ContentInputV1.
        The content's source worksheet

        :param worksheet_id: The worksheet_id of this ContentInputV1.
        :type: str
        """
        if worksheet_id is None:
            raise ValueError("Invalid value for `worksheet_id`, must not be `None`")

        self._worksheet_id = worksheet_id

    @property
    def workstep_id(self):
        """
        Gets the workstep_id of this ContentInputV1.
        The content's source workstep

        :return: The workstep_id of this ContentInputV1.
        :rtype: str
        """
        return self._workstep_id

    @workstep_id.setter
    def workstep_id(self, workstep_id):
        """
        Sets the workstep_id of this ContentInputV1.
        The content's source workstep

        :param workstep_id: The workstep_id of this ContentInputV1.
        :type: str
        """
        if workstep_id is None:
            raise ValueError("Invalid value for `workstep_id`, must not be `None`")

        self._workstep_id = workstep_id

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
        if not isinstance(other, ContentInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

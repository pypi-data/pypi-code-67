# coding: utf-8

"""
    NCBI Datasets API

    NCBI service to query and download biological sequence data across all domains of life from NCBI databases.  # noqa: E501

    The version of the OpenAPI document: v1alpha
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ncbi.datasets.configuration import Configuration


class DownloadSummaryDehydrated(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'cli_download_command_line': 'str',
        'cli_rehydrate_command_line': 'str',
        'estimated_file_size_mb': 'int',
        'url': 'str'
    }

    attribute_map = {
        'cli_download_command_line': 'cli_download_command_line',
        'cli_rehydrate_command_line': 'cli_rehydrate_command_line',
        'estimated_file_size_mb': 'estimated_file_size_mb',
        'url': 'url'
    }

    def __init__(self, cli_download_command_line=None, cli_rehydrate_command_line=None, estimated_file_size_mb=None, url=None, local_vars_configuration=None):  # noqa: E501
        """DownloadSummaryDehydrated - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._cli_download_command_line = None
        self._cli_rehydrate_command_line = None
        self._estimated_file_size_mb = None
        self._url = None
        self.discriminator = None

        if cli_download_command_line is not None:
            self.cli_download_command_line = cli_download_command_line
        if cli_rehydrate_command_line is not None:
            self.cli_rehydrate_command_line = cli_rehydrate_command_line
        if estimated_file_size_mb is not None:
            self.estimated_file_size_mb = estimated_file_size_mb
        if url is not None:
            self.url = url

    @property
    def cli_download_command_line(self):
        """Gets the cli_download_command_line of this DownloadSummaryDehydrated.  # noqa: E501


        :return: The cli_download_command_line of this DownloadSummaryDehydrated.  # noqa: E501
        :rtype: str
        """
        return self._cli_download_command_line

    @cli_download_command_line.setter
    def cli_download_command_line(self, cli_download_command_line):
        """Sets the cli_download_command_line of this DownloadSummaryDehydrated.


        :param cli_download_command_line: The cli_download_command_line of this DownloadSummaryDehydrated.  # noqa: E501
        :type: str
        """

        self._cli_download_command_line = cli_download_command_line

    @property
    def cli_rehydrate_command_line(self):
        """Gets the cli_rehydrate_command_line of this DownloadSummaryDehydrated.  # noqa: E501


        :return: The cli_rehydrate_command_line of this DownloadSummaryDehydrated.  # noqa: E501
        :rtype: str
        """
        return self._cli_rehydrate_command_line

    @cli_rehydrate_command_line.setter
    def cli_rehydrate_command_line(self, cli_rehydrate_command_line):
        """Sets the cli_rehydrate_command_line of this DownloadSummaryDehydrated.


        :param cli_rehydrate_command_line: The cli_rehydrate_command_line of this DownloadSummaryDehydrated.  # noqa: E501
        :type: str
        """

        self._cli_rehydrate_command_line = cli_rehydrate_command_line

    @property
    def estimated_file_size_mb(self):
        """Gets the estimated_file_size_mb of this DownloadSummaryDehydrated.  # noqa: E501


        :return: The estimated_file_size_mb of this DownloadSummaryDehydrated.  # noqa: E501
        :rtype: int
        """
        return self._estimated_file_size_mb

    @estimated_file_size_mb.setter
    def estimated_file_size_mb(self, estimated_file_size_mb):
        """Sets the estimated_file_size_mb of this DownloadSummaryDehydrated.


        :param estimated_file_size_mb: The estimated_file_size_mb of this DownloadSummaryDehydrated.  # noqa: E501
        :type: int
        """

        self._estimated_file_size_mb = estimated_file_size_mb

    @property
    def url(self):
        """Gets the url of this DownloadSummaryDehydrated.  # noqa: E501


        :return: The url of this DownloadSummaryDehydrated.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this DownloadSummaryDehydrated.


        :param url: The url of this DownloadSummaryDehydrated.  # noqa: E501
        :type: str
        """

        self._url = url

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DownloadSummaryDehydrated):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DownloadSummaryDehydrated):
            return True

        return self.to_dict() != other.to_dict()

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


class V1alpha1GeneDescriptors(object):
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
        'errors': 'list[Datasetsv1alpha1Error]',
        'genes': 'list[V1alpha1GeneDescriptor]'
    }

    attribute_map = {
        'errors': 'errors',
        'genes': 'genes'
    }

    def __init__(self, errors=None, genes=None, local_vars_configuration=None):  # noqa: E501
        """V1alpha1GeneDescriptors - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._errors = None
        self._genes = None
        self.discriminator = None

        if errors is not None:
            self.errors = errors
        if genes is not None:
            self.genes = genes

    @property
    def errors(self):
        """Gets the errors of this V1alpha1GeneDescriptors.  # noqa: E501


        :return: The errors of this V1alpha1GeneDescriptors.  # noqa: E501
        :rtype: list[Datasetsv1alpha1Error]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this V1alpha1GeneDescriptors.


        :param errors: The errors of this V1alpha1GeneDescriptors.  # noqa: E501
        :type: list[Datasetsv1alpha1Error]
        """

        self._errors = errors

    @property
    def genes(self):
        """Gets the genes of this V1alpha1GeneDescriptors.  # noqa: E501


        :return: The genes of this V1alpha1GeneDescriptors.  # noqa: E501
        :rtype: list[V1alpha1GeneDescriptor]
        """
        return self._genes

    @genes.setter
    def genes(self, genes):
        """Sets the genes of this V1alpha1GeneDescriptors.


        :param genes: The genes of this V1alpha1GeneDescriptors.  # noqa: E501
        :type: list[V1alpha1GeneDescriptor]
        """

        self._genes = genes

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
        if not isinstance(other, V1alpha1GeneDescriptors):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1alpha1GeneDescriptors):
            return True

        return self.to_dict() != other.to_dict()

# coding: utf-8

"""
    Thoth User API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.6.0-dev

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class InlineResponse2001HardwareEnvironments(object):
    """NOTE: This class is auto generated by the swagger code generator program.

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
        "cpu_cores": "int",
        "cpu_family": "int",
        "cpu_model": "int",
        "cpu_model_name": "str",
        "cpu_physical_cpus": "int",
        "cpu_vendor": "int",
        "gpu_cores": "int",
        "gpu_memory_size": "int",
        "gpu_model_name": "str",
        "gpu_vendor": "str",
        "ram_size": "int",
    }

    attribute_map = {
        "cpu_cores": "cpu_cores",
        "cpu_family": "cpu_family",
        "cpu_model": "cpu_model",
        "cpu_model_name": "cpu_model_name",
        "cpu_physical_cpus": "cpu_physical_cpus",
        "cpu_vendor": "cpu_vendor",
        "gpu_cores": "gpu_cores",
        "gpu_memory_size": "gpu_memory_size",
        "gpu_model_name": "gpu_model_name",
        "gpu_vendor": "gpu_vendor",
        "ram_size": "ram_size",
    }

    def __init__(
        self,
        cpu_cores=None,
        cpu_family=None,
        cpu_model=None,
        cpu_model_name=None,
        cpu_physical_cpus=None,
        cpu_vendor=None,
        gpu_cores=None,
        gpu_memory_size=None,
        gpu_model_name=None,
        gpu_vendor=None,
        ram_size=None,
    ):  # noqa: E501
        """InlineResponse2001HardwareEnvironments - a model defined in Swagger"""  # noqa: E501
        self._cpu_cores = None
        self._cpu_family = None
        self._cpu_model = None
        self._cpu_model_name = None
        self._cpu_physical_cpus = None
        self._cpu_vendor = None
        self._gpu_cores = None
        self._gpu_memory_size = None
        self._gpu_model_name = None
        self._gpu_vendor = None
        self._ram_size = None
        self.discriminator = None
        self.cpu_cores = cpu_cores
        self.cpu_family = cpu_family
        self.cpu_model = cpu_model
        self.cpu_model_name = cpu_model_name
        self.cpu_physical_cpus = cpu_physical_cpus
        self.cpu_vendor = cpu_vendor
        self.gpu_cores = gpu_cores
        self.gpu_memory_size = gpu_memory_size
        self.gpu_model_name = gpu_model_name
        self.gpu_vendor = gpu_vendor
        self.ram_size = ram_size

    @property
    def cpu_cores(self):
        """Gets the cpu_cores of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        Number of cores of the CPU.  # noqa: E501

        :return: The cpu_cores of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: int
        """
        return self._cpu_cores

    @cpu_cores.setter
    def cpu_cores(self, cpu_cores):
        """Sets the cpu_cores of this InlineResponse2001HardwareEnvironments.

        Number of cores of the CPU.  # noqa: E501

        :param cpu_cores: The cpu_cores of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: int
        """
        if cpu_cores is None:
            raise ValueError(
                "Invalid value for `cpu_cores`, must not be `None`"
            )  # noqa: E501

        self._cpu_cores = cpu_cores

    @property
    def cpu_family(self):
        """Gets the cpu_family of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        The CPU family.  # noqa: E501

        :return: The cpu_family of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: int
        """
        return self._cpu_family

    @cpu_family.setter
    def cpu_family(self, cpu_family):
        """Sets the cpu_family of this InlineResponse2001HardwareEnvironments.

        The CPU family.  # noqa: E501

        :param cpu_family: The cpu_family of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: int
        """
        if cpu_family is None:
            raise ValueError(
                "Invalid value for `cpu_family`, must not be `None`"
            )  # noqa: E501

        self._cpu_family = cpu_family

    @property
    def cpu_model(self):
        """Gets the cpu_model of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        The CPU model.  # noqa: E501

        :return: The cpu_model of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: int
        """
        return self._cpu_model

    @cpu_model.setter
    def cpu_model(self, cpu_model):
        """Sets the cpu_model of this InlineResponse2001HardwareEnvironments.

        The CPU model.  # noqa: E501

        :param cpu_model: The cpu_model of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: int
        """
        if cpu_model is None:
            raise ValueError(
                "Invalid value for `cpu_model`, must not be `None`"
            )  # noqa: E501

        self._cpu_model = cpu_model

    @property
    def cpu_model_name(self):
        """Gets the cpu_model_name of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        The CPU model name.  # noqa: E501

        :return: The cpu_model_name of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._cpu_model_name

    @cpu_model_name.setter
    def cpu_model_name(self, cpu_model_name):
        """Sets the cpu_model_name of this InlineResponse2001HardwareEnvironments.

        The CPU model name.  # noqa: E501

        :param cpu_model_name: The cpu_model_name of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: str
        """
        if cpu_model_name is None:
            raise ValueError(
                "Invalid value for `cpu_model_name`, must not be `None`"
            )  # noqa: E501

        self._cpu_model_name = cpu_model_name

    @property
    def cpu_physical_cpus(self):
        """Gets the cpu_physical_cpus of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        The CPU physical CPUs.  # noqa: E501

        :return: The cpu_physical_cpus of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: int
        """
        return self._cpu_physical_cpus

    @cpu_physical_cpus.setter
    def cpu_physical_cpus(self, cpu_physical_cpus):
        """Sets the cpu_physical_cpus of this InlineResponse2001HardwareEnvironments.

        The CPU physical CPUs.  # noqa: E501

        :param cpu_physical_cpus: The cpu_physical_cpus of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: int
        """
        if cpu_physical_cpus is None:
            raise ValueError(
                "Invalid value for `cpu_physical_cpus`, must not be `None`"
            )  # noqa: E501

        self._cpu_physical_cpus = cpu_physical_cpus

    @property
    def cpu_vendor(self):
        """Gets the cpu_vendor of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        The CPU vendor.  # noqa: E501

        :return: The cpu_vendor of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: int
        """
        return self._cpu_vendor

    @cpu_vendor.setter
    def cpu_vendor(self, cpu_vendor):
        """Sets the cpu_vendor of this InlineResponse2001HardwareEnvironments.

        The CPU vendor.  # noqa: E501

        :param cpu_vendor: The cpu_vendor of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: int
        """
        if cpu_vendor is None:
            raise ValueError(
                "Invalid value for `cpu_vendor`, must not be `None`"
            )  # noqa: E501

        self._cpu_vendor = cpu_vendor

    @property
    def gpu_cores(self):
        """Gets the gpu_cores of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        Number of cores of the GPU.  # noqa: E501

        :return: The gpu_cores of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: int
        """
        return self._gpu_cores

    @gpu_cores.setter
    def gpu_cores(self, gpu_cores):
        """Sets the gpu_cores of this InlineResponse2001HardwareEnvironments.

        Number of cores of the GPU.  # noqa: E501

        :param gpu_cores: The gpu_cores of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: int
        """
        if gpu_cores is None:
            raise ValueError(
                "Invalid value for `gpu_cores`, must not be `None`"
            )  # noqa: E501

        self._gpu_cores = gpu_cores

    @property
    def gpu_memory_size(self):
        """Gets the gpu_memory_size of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        The GPU memory size.  # noqa: E501

        :return: The gpu_memory_size of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: int
        """
        return self._gpu_memory_size

    @gpu_memory_size.setter
    def gpu_memory_size(self, gpu_memory_size):
        """Sets the gpu_memory_size of this InlineResponse2001HardwareEnvironments.

        The GPU memory size.  # noqa: E501

        :param gpu_memory_size: The gpu_memory_size of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: int
        """
        if gpu_memory_size is None:
            raise ValueError(
                "Invalid value for `gpu_memory_size`, must not be `None`"
            )  # noqa: E501

        self._gpu_memory_size = gpu_memory_size

    @property
    def gpu_model_name(self):
        """Gets the gpu_model_name of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        The GPU model name.  # noqa: E501

        :return: The gpu_model_name of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._gpu_model_name

    @gpu_model_name.setter
    def gpu_model_name(self, gpu_model_name):
        """Sets the gpu_model_name of this InlineResponse2001HardwareEnvironments.

        The GPU model name.  # noqa: E501

        :param gpu_model_name: The gpu_model_name of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: str
        """
        if gpu_model_name is None:
            raise ValueError(
                "Invalid value for `gpu_model_name`, must not be `None`"
            )  # noqa: E501

        self._gpu_model_name = gpu_model_name

    @property
    def gpu_vendor(self):
        """Gets the gpu_vendor of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        The GPU vendor.  # noqa: E501

        :return: The gpu_vendor of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._gpu_vendor

    @gpu_vendor.setter
    def gpu_vendor(self, gpu_vendor):
        """Sets the gpu_vendor of this InlineResponse2001HardwareEnvironments.

        The GPU vendor.  # noqa: E501

        :param gpu_vendor: The gpu_vendor of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: str
        """
        if gpu_vendor is None:
            raise ValueError(
                "Invalid value for `gpu_vendor`, must not be `None`"
            )  # noqa: E501

        self._gpu_vendor = gpu_vendor

    @property
    def ram_size(self):
        """Gets the ram_size of this InlineResponse2001HardwareEnvironments.  # noqa: E501

        The RAM size.  # noqa: E501

        :return: The ram_size of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :rtype: int
        """
        return self._ram_size

    @ram_size.setter
    def ram_size(self, ram_size):
        """Sets the ram_size of this InlineResponse2001HardwareEnvironments.

        The RAM size.  # noqa: E501

        :param ram_size: The ram_size of this InlineResponse2001HardwareEnvironments.  # noqa: E501
        :type: int
        """
        if ram_size is None:
            raise ValueError(
                "Invalid value for `ram_size`, must not be `None`"
            )  # noqa: E501

        self._ram_size = ram_size

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(InlineResponse2001HardwareEnvironments, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, InlineResponse2001HardwareEnvironments):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

# coding: utf-8

"""
    IBM Watson Machine Learning REST API

    ## Authorization  ### IBM Watson Machine Learning Credentials  To start working with API one needs to generate an `access token` using the `username` and `password` available on the Service Credentials tab of the IBM Watson Machine Learning service instance or also available in the VCAP environment variable.  Example of the Service Credentials:  ```json {     \"url\": \"https://ibm-watson-ml.mybluemix.net\",     \"access_key\": \"ERY9vcBfE4sE+F4g8hcotF9L+j81WXWeZv\",     \"username\": \"c1ef4b80-2ee2-458e-ab92-e9ca97ec657d\",     \"password\": \"030528d4-5a3e-4d4c-9258-5d553513be6f\" } ```  Example of obtaining `access token` from Token Endpoint using HTTP Basic Auth (for details please refer to Token section below):  ` curl --basic --user username:password https://ibm-watson-ml.mybluemix.net/v2/identity/token `   ### Apache Spark Service Credentials  The IBM Watson Machine Learning co-operates with the Apache Spark as a Service to deploy pipeline models. For API methods requiring Apache Spark Service instance a custom header: `X-Spark-Service-Instance` with Service Credentials must be specified. The header value is a **base64 encoded** string with the Service Credentials JSON data.  [Example of API method requiring Apache Spark Service](https://console.ng.bluemix.net/docs/services/PredictiveModeling/index-gentopic1.html#pm_service_api_spark_batch) 

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

#  (C) Copyright IBM Corp. 2020.
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#       http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from pprint import pformat
from six import iteritems
import re


class EvaluationDefinitionMetrics(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, threshold=None):
        """
        EvaluationDefinitionMetrics - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'threshold': 'float'
        }

        self.attribute_map = {
            'name': 'name',
            'threshold': 'threshold'
        }

        self._name = name
        self._threshold = threshold

    @property
    def name(self):
        """
        Gets the name of this EvaluationDefinitionMetrics.
        The name of the metric

        :return: The name of this EvaluationDefinitionMetrics.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this EvaluationDefinitionMetrics.
        The name of the metric

        :param name: The name of this EvaluationDefinitionMetrics.
        :type: str
        """

        self._name = name

    @property
    def threshold(self):
        """
        Gets the threshold of this EvaluationDefinitionMetrics.
        The threshold value for the metric

        :return: The threshold of this EvaluationDefinitionMetrics.
        :rtype: float
        """
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        """
        Sets the threshold of this EvaluationDefinitionMetrics.
        The threshold value for the metric

        :param threshold: The threshold of this EvaluationDefinitionMetrics.
        :type: float
        """

        self._threshold = threshold

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
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

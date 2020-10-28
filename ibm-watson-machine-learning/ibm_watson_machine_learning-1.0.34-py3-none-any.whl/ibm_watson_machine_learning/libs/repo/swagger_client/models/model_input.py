# coding: utf-8

"""
    IBM Watson Machine Learning REST API

    ## Authorization  ### IBM Watson Machine Learning Credentials (ML Credentials)  The IBM Watson Machine Learning Credentials are available for the Bluemix user for each bound application or requested service key. You will find them in the VCAP information as well you can access them using Cloud Foundry API.  Here is the example of the ML Credentials:  ```json {   \"url\": \"https://ibm-watson-ml.mybluemix.net\",   \"username\": \"c1ef4b80-2ee2-458e-ab92-e9ca97ec657d\",   \"password\": \"edb699da-8595-406e-bae0-74a834fa4d34\",    \"access_key\": \"0uUQPsbQozcci4uwRI7xo0jQnSNOM9YSk....\" } ```  - `url` - the base WML API url - `username` / `password` - the service credentials required to generate the token - `access_key` - the access key used by previous version of the service API (ignored)  The `username` / `password` pair are used to access the Token Endpoint (using HTTP Basic Auth) and obtain the service token (see below). Example:  `curl --basic --user c1ef4b80-2ee2-458e-ab92-e9ca97ec657d:edb699da-8595-406e-bae0-74a834fa4d34 https://ibm-watson-ml.mybluemix.net/v2/identity/token`  ### IBM Watson Machine Learning Token (ML Token)  The IBM Watson Machine Learning REST API is authorized with ML token obtained from the Token Endpoint. The ML token is used as a baerer token send in `authorization` header.  Use WML service credentials (username, password) to gather the token from:   `/v2/identity/token` (see example above).  The token is self-describing JWT (JSON Web Tokens) protected by digital signature for authentication. It holds information required for a service tenant identification. Each ML micro-service is able to verify the token with the public key without request to the token endpoint and firing a database query. The ML service token (ML token) contains the expiration time what simplifies implementation of the access revocation.  ## Spark Instance  The IBM Watson ML co-operates with the Spark as a Service to make calculation and deploy pipeline models. Each API method that requires the Spark service instance accepts a custom header: `X-Spark-Service-Instance` where the Spark instance data like credentials, kernel ID and version can be specified. The header value is a base64 encoded string with the JSON data in the following format:    ```   {     \"credentials\": {       \"tenant_id\": \"sf2c-xxxxx-05b1d10fb12b\",       \"cluster_master_url\": \"https://spark.stage1.bluemix.net\",       \"tenant_id_full\": \"xxxxx-a94d-4f20-bf2c-xxxxxx-xxxx-4c65-a156-05b1d10fb12b\",       \"tenant_secret\": \"xxxx-86fd-40cd-xxx-969aafaeb505\",       \"instance_id\": \"xxx-a94d-xxx-bf2c-xxxx\",       \"plan\": \"ibm.SparkService.PayGoPersonal\"     },     \"version\": \"2.0\",     \"kernelId\": \"xxx-a94d-xxx-bf2c-xxxx\"   }   ```  The fields are: - `credentials` - from the VCAP information of the Spark service instance - `version` - requested Spark version (possible values: 2.0) - `kernelId` (optional) - the Spark kernel ID is only required by actions that operates on running Spark kernel.   This field is redundant when creating any kind of deployment. 

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


class ModelInput(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None, author=None, pipeline_version_href=None, type=None, runtime_environment=None, training_data_schema=None, label_col=None, input_data_schema=None, output_data_schema=None):
        """
        ModelInput - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'description': 'str',
            'author': 'ArtifactAuthor',
            'pipeline_version_href': 'str',
            'type': 'ModelType',
            'runtime_environment': 'RuntimeEnvironment',
            'training_data_schema': 'object',
            'label_col': 'str',
            'input_data_schema': 'object',
            'output_data_schema': 'object'
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'author': 'author',
            'pipeline_version_href': 'pipelineVersionHref',
            'type': 'type',
            'runtime_environment': 'runtimeEnvironment',
            'training_data_schema': 'trainingDataSchema',
            'label_col': 'labelCol',
            'input_data_schema': 'inputDataSchema',
            'output_data_schema': 'outputDataSchema'
        }

        self._name = name
        self._description = description
        self._author = author
        self._pipeline_version_href = pipeline_version_href
        self._type = type
        self._runtime_environment = runtime_environment
        self._training_data_schema = training_data_schema
        self._label_col = label_col
        self._input_data_schema = input_data_schema
        self._output_data_schema = output_data_schema

    @property
    def name(self):
        """
        Gets the name of this ModelInput.
        Name of the model

        :return: The name of this ModelInput.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ModelInput.
        Name of the model

        :param name: The name of this ModelInput.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ModelInput.
        Description of the model

        :return: The description of this ModelInput.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ModelInput.
        Description of the model

        :param description: The description of this ModelInput.
        :type: str
        """

        self._description = description

    @property
    def author(self):
        """
        Gets the author of this ModelInput.
        Author of the pipeline

        :return: The author of this ModelInput.
        :rtype: ArtifactAuthor
        """
        return self._author

    @author.setter
    def author(self, author):
        """
        Sets the author of this ModelInput.
        Author of the pipeline

        :param author: The author of this ModelInput.
        :type: ArtifactAuthor
        """

        self._author = author

    @property
    def pipeline_version_href(self):
        """
        Gets the pipeline_version_href of this ModelInput.
        Href of the pipeline version from which the model was created.

        :return: The pipeline_version_href of this ModelInput.
        :rtype: str
        """
        return self._pipeline_version_href

    @pipeline_version_href.setter
    def pipeline_version_href(self, pipeline_version_href):
        """
        Sets the pipeline_version_href of this ModelInput.
        Href of the pipeline version from which the model was created.

        :param pipeline_version_href: The pipeline_version_href of this ModelInput.
        :type: str
        """

        self._pipeline_version_href = pipeline_version_href

    @property
    def type(self):
        """
        Gets the type of this ModelInput.


        :return: The type of this ModelInput.
        :rtype: ModelType
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ModelInput.


        :param type: The type of this ModelInput.
        :type: ModelType
        """

        self._type = type

    @property
    def runtime_environment(self):
        """
        Gets the runtime_environment of this ModelInput.


        :return: The runtime_environment of this ModelInput.
        :rtype: RuntimeEnvironment
        """
        return self._runtime_environment

    @runtime_environment.setter
    def runtime_environment(self, runtime_environment):
        """
        Sets the runtime_environment of this ModelInput.


        :param runtime_environment: The runtime_environment of this ModelInput.
        :type: RuntimeEnvironment
        """

        self._runtime_environment = runtime_environment

    @property
    def training_data_schema(self):
        """
        Gets the training_data_schema of this ModelInput.
        JSON schema of the training data

        :return: The training_data_schema of this ModelInput.
        :rtype: TrainingDataSchema
        """
        return self._training_data_schema

    @training_data_schema.setter
    def training_data_schema(self, training_data_schema):
        """
        Sets the training_data_schema of this ModelInput.
        JSON schema of the training data

        :param training_data_schema: The training_data_schema of this ModelInput.
        :type: TrainingDataSchema
        """

        self._training_data_schema = training_data_schema

    @property
    def label_col(self):
        """
        Gets the label_col of this ModelInput.
        Name of the label column

        :return: The label_col of this ModelInput.
        :rtype: str
        """
        return self._label_col

    @label_col.setter
    def label_col(self, label_col):
        """
        Sets the label_col of this ModelInput.
        Name of the label column

        :param label_col: The label_col of this ModelInput.
        :type: str
        """

        self._label_col = label_col

    @property
    def input_data_schema(self):
        """
        Gets the input_data_schema of this ModelInput.
        JSON schema of the input data (if not provided the training data schema is used)

        :return: The input_data_schema of this ModelInput.
        :rtype: InputDataSchema
        """
        return self._input_data_schema

    @input_data_schema.setter
    def input_data_schema(self, input_data_schema):
        """
        Sets the input_data_schema of this ModelInput.
        JSON schema of the input data (if not provided the training data schema is used)

        :param input_data_schema: The input_data_schema of this ModelInput.
        :type: InputDataSchema
        """

        self._input_data_schema = input_data_schema

    @property
    def output_data_schema(self):
        """
        Gets the output_data_schema of this ModelInput.
        JSON schema of the output data

        :return: The output_data_schema of this ModelInput.
        :rtype: OutputDataSchema
        """
        return self._output_data_schema

    @output_data_schema.setter
    def output_data_schema(self, output_data_schema):
        """
        Sets the output_data_schema of this ModelInput.
        JSON schema of the output data

        :param output_data_schema: The output_data_schema of this ModelInput.
        :type: OutputDataSchema
        """

        self._output_data_schema = output_data_schema

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

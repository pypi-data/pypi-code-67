# coding: utf-8

"""
    Aliro Quantum App

    This is an api for the Aliro Quantum App  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import aliro_quantum
from aliro_quantum.models.credentials_rigetti import CredentialsRigetti  # noqa: E501
from aliro_quantum.rest import ApiException

class TestCredentialsRigetti(unittest.TestCase):
    """CredentialsRigetti unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CredentialsRigetti
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = aliro_quantum.models.credentials_rigetti.CredentialsRigetti()  # noqa: E501
        if include_optional :
            return CredentialsRigetti(
                machine_host = '0', 
                rsa_private_key = '0', 
                use_aliro = True
            )
        else :
            return CredentialsRigetti(
                machine_host = '0',
                rsa_private_key = '0',
        )

    def testCredentialsRigetti(self):
        """Test CredentialsRigetti"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

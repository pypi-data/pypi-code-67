# coding: utf-8

"""
    Red Rover API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1
    Contact: contact@edustaff.org
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import redrover_api
from redrover_api.models.struct_layout_attribute import StructLayoutAttribute  # noqa: E501
from redrover_api.rest import ApiException

class TestStructLayoutAttribute(unittest.TestCase):
    """StructLayoutAttribute unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test StructLayoutAttribute
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = redrover_api.models.struct_layout_attribute.StructLayoutAttribute()  # noqa: E501
        if include_optional :
            return StructLayoutAttribute(
                value = 0, 
                type_id = redrover_api.models.type_id.typeId()
            )
        else :
            return StructLayoutAttribute(
        )

    def testStructLayoutAttribute(self):
        """Test StructLayoutAttribute"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_deb
from pulpcore.client.pulp_deb.models.paginateddeb_apt_remote_response_list import PaginateddebAptRemoteResponseList  # noqa: E501
from pulpcore.client.pulp_deb.rest import ApiException

class TestPaginateddebAptRemoteResponseList(unittest.TestCase):
    """PaginateddebAptRemoteResponseList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginateddebAptRemoteResponseList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_deb.models.paginateddeb_apt_remote_response_list.PaginateddebAptRemoteResponseList()  # noqa: E501
        if include_optional :
            return PaginateddebAptRemoteResponseList(
                count = 123, 
                next = 'http://api.example.org/accounts/?offset=400&limit=100', 
                previous = 'http://api.example.org/accounts/?offset=200&limit=100', 
                results = [
                    pulpcore.client.pulp_deb.models.deb/apt_remote_response.deb.AptRemoteResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        name = '0', 
                        url = '0', 
                        ca_cert = '0', 
                        client_cert = '0', 
                        client_key = '0', 
                        tls_validation = True, 
                        proxy_url = '0', 
                        username = '0', 
                        password = '0', 
                        pulp_last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        download_concurrency = 1, 
                        policy = null, 
                        distributions = '0', 
                        components = '0', 
                        architectures = '0', 
                        sync_sources = True, 
                        sync_udebs = True, 
                        sync_installer = True, 
                        gpgkey = '0', )
                    ]
            )
        else :
            return PaginateddebAptRemoteResponseList(
        )

    def testPaginateddebAptRemoteResponseList(self):
        """Test PaginateddebAptRemoteResponseList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

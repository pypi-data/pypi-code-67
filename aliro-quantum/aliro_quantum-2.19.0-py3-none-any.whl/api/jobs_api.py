# coding: utf-8

"""
    Aliro Quantum App

    This is an api for the Aliro Quantum App  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from aliro_quantum.api_client import ApiClient
from aliro_quantum.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class JobsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def jobs_cancel_job_id_post(self, job_id, **kwargs):  # noqa: E501
        """cancel job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.jobs_cancel_job_id_post(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str job_id: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: BasicSuccess
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.jobs_cancel_job_id_post_with_http_info(job_id, **kwargs)  # noqa: E501

    def jobs_cancel_job_id_post_with_http_info(self, job_id, **kwargs):  # noqa: E501
        """cancel job  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.jobs_cancel_job_id_post_with_http_info(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str job_id: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(BasicSuccess, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'job_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method jobs_cancel_job_id_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'job_id' is set
        if self.api_client.client_side_validation and ('job_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['job_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `job_id` when calling `jobs_cancel_job_id_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'job_id' in local_var_params:
            path_params['jobId'] = local_var_params['job_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['JwtKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/jobs/cancel/{jobId}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BasicSuccess',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

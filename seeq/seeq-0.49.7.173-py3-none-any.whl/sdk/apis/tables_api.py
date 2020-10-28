# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.49.07-BETA
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient
from ..models import *

class TablesApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def build(self, **kwargs):
        """
        Build a table
        Pagination is enabled for this query
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.build(start=start_value, end=end_value, condition_ids=condition_ids_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str start: The start time of the capsule inputs for the table. (required)
        :param str end: The end time of the capsule inputs for the table. (required)
        :param list[str] condition_ids: The IDs of the conditions that will be used to create table rows. (required)
        :param list[str] column_definitions: A list of column definitions for the table, where a column definition is: \"formula ON id AS name\" where id and name are optional. If id is supplied, the formula can reference it using the \"$series\" variable (e.g. $series.max()). If id is not supplied the calculation is assumed to act on the capsules that define each row and the formula should reference the \"$capsule\" variable (e.g. $capsule.duration()).
        :param list[str] sort_orders: A list of sort orders for the table, where a sort order is the column index, starting at 0, followed by a space and a sort direction of either \"asc\" or \"desc\". 0 is Capsule ID, 1 is Capsule Is Uncertain, 2 is Condition ID, 3 is Capsule Start Key, 4 is Capsule End Key, and any index above 4 comes from the input columnDefinitions.
        :param int offset: The row offset into the table results. The default offset is 0. Large row offsets may result in out of memory errors.
        :param int limit: The pagination limit, the total number of collection items that will be returned in this page of results
        :return: TableOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: TableOutputV1
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.build_with_http_info(**kwargs)
        else:
            (data) = self.build_with_http_info(**kwargs)
            return data

    def build_with_http_info(self, **kwargs):
        """
        Build a table
        Pagination is enabled for this query
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.build_with_http_info(start=start_value, end=end_value, condition_ids=condition_ids_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str start: The start time of the capsule inputs for the table. (required)
        :param str end: The end time of the capsule inputs for the table. (required)
        :param list[str] condition_ids: The IDs of the conditions that will be used to create table rows. (required)
        :param list[str] column_definitions: A list of column definitions for the table, where a column definition is: \"formula ON id AS name\" where id and name are optional. If id is supplied, the formula can reference it using the \"$series\" variable (e.g. $series.max()). If id is not supplied the calculation is assumed to act on the capsules that define each row and the formula should reference the \"$capsule\" variable (e.g. $capsule.duration()).
        :param list[str] sort_orders: A list of sort orders for the table, where a sort order is the column index, starting at 0, followed by a space and a sort direction of either \"asc\" or \"desc\". 0 is Capsule ID, 1 is Capsule Is Uncertain, 2 is Condition ID, 3 is Capsule Start Key, 4 is Capsule End Key, and any index above 4 comes from the input columnDefinitions.
        :param int offset: The row offset into the table results. The default offset is 0. Large row offsets may result in out of memory errors.
        :param int limit: The pagination limit, the total number of collection items that will be returned in this page of results
        :return: TableOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: TableOutputV1
        """

        all_params = ['start', 'end', 'condition_ids', 'column_definitions', 'sort_orders', 'offset', 'limit']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method build" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'start' is set
        if ('start' not in params) or (params['start'] is None):
            raise ValueError("Missing the required parameter `start` when calling `build`")
        # verify the required parameter 'end' is set
        if ('end' not in params) or (params['end'] is None):
            raise ValueError("Missing the required parameter `end` when calling `build`")
        # verify the required parameter 'condition_ids' is set
        if ('condition_ids' not in params) or (params['condition_ids'] is None):
            raise ValueError("Missing the required parameter `condition_ids` when calling `build`")


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'start' in params:
            query_params.append(('start', params['start']))
        if 'end' in params:
            query_params.append(('end', params['end']))
        if 'condition_ids' in params:
            query_params.append(('conditionIds', params['condition_ids']))
            collection_formats['conditionIds'] = 'multi'
        if 'column_definitions' in params:
            query_params.append(('columnDefinitions', params['column_definitions']))
            collection_formats['columnDefinitions'] = 'multi'
        if 'sort_orders' in params:
            query_params.append(('sortOrders', params['sort_orders']))
            collection_formats['sortOrders'] = 'multi'
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'limit' in params:
            query_params.append(('limit', params['limit']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/vnd.seeq.v1+json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/vnd.seeq.v1+json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api('/tables/build', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='TableOutputV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

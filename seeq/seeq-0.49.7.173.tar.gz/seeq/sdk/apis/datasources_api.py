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

class DatasourcesApi(object):
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

    def clean_up(self, **kwargs):
        """
        Archive stale hosted items
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.clean_up(id=id_value, body=body_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource to clean up (required)
        :param DatasourceCleanUpInputV1 body: Input parameters for the Datasource clean-up process (required)
        :return: DatasourceCleanUpOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceCleanUpOutputV1
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.clean_up_with_http_info(**kwargs)
        else:
            (data) = self.clean_up_with_http_info(**kwargs)
            return data

    def clean_up_with_http_info(self, **kwargs):
        """
        Archive stale hosted items
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.clean_up_with_http_info(id=id_value, body=body_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource to clean up (required)
        :param DatasourceCleanUpInputV1 body: Input parameters for the Datasource clean-up process (required)
        :return: DatasourceCleanUpOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceCleanUpOutputV1
        """

        all_params = ['id', 'body']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clean_up" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `clean_up`")
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `clean_up`")


        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/vnd.seeq.v1+json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/vnd.seeq.v1+json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api('/datasources/{id}/cleanup', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='DatasourceCleanUpOutputV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def create_datasource(self, **kwargs):
        """
        Create a datasource
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_datasource(body=body_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param DatasourceInputV1 body: Datasource information (required)
        :return: DatasourceOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceOutputV1
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.create_datasource_with_http_info(**kwargs)
        else:
            (data) = self.create_datasource_with_http_info(**kwargs)
            return data

    def create_datasource_with_http_info(self, **kwargs):
        """
        Create a datasource
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.create_datasource_with_http_info(body=body_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param DatasourceInputV1 body: Datasource information (required)
        :return: DatasourceOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceOutputV1
        """

        all_params = ['body']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_datasource" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_datasource`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/vnd.seeq.v1+json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/vnd.seeq.v1+json'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api('/datasources', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='DatasourceOutputV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def delete_datasource(self, **kwargs):
        """
        Archive a datasource
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_datasource(id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource to delete (required)
        :return: StatusMessageBase
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: StatusMessageBase
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.delete_datasource_with_http_info(**kwargs)
        else:
            (data) = self.delete_datasource_with_http_info(**kwargs)
            return data

    def delete_datasource_with_http_info(self, **kwargs):
        """
        Archive a datasource
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_datasource_with_http_info(id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource to delete (required)
        :return: StatusMessageBase
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: StatusMessageBase
        """

        all_params = ['id']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_datasource" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_datasource`")


        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []

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

        return self.api_client.call_api('/datasources/{id}', 'DELETE',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='StatusMessageBase',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_datasource(self, **kwargs):
        """
        Get a Datasource
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_datasource(id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource to retrieve (required)
        :return: DatasourceOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceOutputV1
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_datasource_with_http_info(**kwargs)
        else:
            (data) = self.get_datasource_with_http_info(**kwargs)
            return data

    def get_datasource_with_http_info(self, **kwargs):
        """
        Get a Datasource
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_datasource_with_http_info(id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource to retrieve (required)
        :return: DatasourceOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceOutputV1
        """

        all_params = ['id']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_datasource" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_datasource`")


        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []

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

        return self.api_client.call_api('/datasources/{id}', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='DatasourceOutputV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_datasources(self, **kwargs):
        """
        Get a collection of datasources
        Pagination is enabled for this query
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_datasources(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str datasource_class: The datasource class, the name of the underlying source, 'CSV File' for example, not specifying this parameter will return datasources of any class
        :param str datasource_id: The datasource ID, an identifier that distinguishes a datasource from others of the same datasource class, 'timeseries/salt' for example, not specifying this parameter will return datasources of any ID
        :param int offset: The pagination offset, the index of the first collection item that will be returned in this page of results
        :param int limit: The pagination limit, the total number of collection items that will be returned in this page of results
        :param bool include_archived: Whether archived datasources should be included
        :return: DatasourceOutputListV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceOutputListV1
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_datasources_with_http_info(**kwargs)
        else:
            (data) = self.get_datasources_with_http_info(**kwargs)
            return data

    def get_datasources_with_http_info(self, **kwargs):
        """
        Get a collection of datasources
        Pagination is enabled for this query
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_datasources_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str datasource_class: The datasource class, the name of the underlying source, 'CSV File' for example, not specifying this parameter will return datasources of any class
        :param str datasource_id: The datasource ID, an identifier that distinguishes a datasource from others of the same datasource class, 'timeseries/salt' for example, not specifying this parameter will return datasources of any ID
        :param int offset: The pagination offset, the index of the first collection item that will be returned in this page of results
        :param int limit: The pagination limit, the total number of collection items that will be returned in this page of results
        :param bool include_archived: Whether archived datasources should be included
        :return: DatasourceOutputListV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceOutputListV1
        """

        all_params = ['datasource_class', 'datasource_id', 'offset', 'limit', 'include_archived']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_datasources" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        path_params = {}

        query_params = []
        if 'datasource_class' in params:
            query_params.append(('datasourceClass', params['datasource_class']))
        if 'datasource_id' in params:
            query_params.append(('datasourceId', params['datasource_id']))
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'include_archived' in params:
            query_params.append(('includeArchived', params['include_archived']))

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

        return self.api_client.call_api('/datasources', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='DatasourceOutputListV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_items_hosted_by_datasource(self, **kwargs):
        """
        Get a list of the items hosted by this datasource
        Pagination is enabled for this query
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_items_hosted_by_datasource(id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource (required)
        :param str data_id: The dataId for a specific hosted item
        :param int offset: The pagination offset, the index of the first collection item that will be returned in this page of results
        :param int limit: The pagination limit, the total number of collection items that will be returned in this page of results
        :return: ItemPreviewListV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: ItemPreviewListV1
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_items_hosted_by_datasource_with_http_info(**kwargs)
        else:
            (data) = self.get_items_hosted_by_datasource_with_http_info(**kwargs)
            return data

    def get_items_hosted_by_datasource_with_http_info(self, **kwargs):
        """
        Get a list of the items hosted by this datasource
        Pagination is enabled for this query
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_items_hosted_by_datasource_with_http_info(id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource (required)
        :param str data_id: The dataId for a specific hosted item
        :param int offset: The pagination offset, the index of the first collection item that will be returned in this page of results
        :param int limit: The pagination limit, the total number of collection items that will be returned in this page of results
        :return: ItemPreviewListV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: ItemPreviewListV1
        """

        all_params = ['id', 'data_id', 'offset', 'limit']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_items_hosted_by_datasource" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_items_hosted_by_datasource`")


        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []
        if 'data_id' in params:
            query_params.append(('dataId', params['data_id']))
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

        return self.api_client.call_api('/datasources/{id}/items', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='ItemPreviewListV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def get_status(self, **kwargs):
        """
        Get statistics describing the health of remote datasources
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_status(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: DatasourceStatusOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceStatusOutputV1
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.get_status_with_http_info(**kwargs)
        else:
            (data) = self.get_status_with_http_info(**kwargs)
            return data

    def get_status_with_http_info(self, **kwargs):
        """
        Get statistics describing the health of remote datasources
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_status_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: DatasourceStatusOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceStatusOutputV1
        """

        all_params = []
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_status" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

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

        return self.api_client.call_api('/datasources/status', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='DatasourceStatusOutputV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def recount(self, **kwargs):
        """
        Recount item totals for a datasource. Do not run while datasource is indexing
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.recount(id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource to recount (required)
        :return: DatasourceOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceOutputV1
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.recount_with_http_info(**kwargs)
        else:
            (data) = self.recount_with_http_info(**kwargs)
            return data

    def recount_with_http_info(self, **kwargs):
        """
        Recount item totals for a datasource. Do not run while datasource is indexing
        
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.recount_with_http_info(id=id_value, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str id: ID of the datasource to recount (required)
        :return: DatasourceOutputV1
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DatasourceOutputV1
        """

        all_params = ['id']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method recount" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params) or (params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `recount`")


        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']

        query_params = []

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

        return self.api_client.call_api('/datasources/{id}/recount', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='DatasourceOutputV1',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

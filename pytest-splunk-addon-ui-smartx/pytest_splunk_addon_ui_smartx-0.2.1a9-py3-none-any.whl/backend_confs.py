# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
from .utils import backend_retry
import requests
from requests.auth import HTTPBasicAuth
import urllib.request, urllib.parse, urllib.error

class BackendConf(object):
    """
    Base Class to fetch configurations from rest endpoint. The classes need management url & session_id of the splunk to fetch the configurations.
    """
    def __init__(self, url, username, password):
        """
            :param url: management url of the Splunk instance.
            :param username: username of the Splunk instance
            :param password: password of the Splunk instance
        """
        self.url = url
        self.username = username
        self.password = password

    @backend_retry(3)
    def rest_call(self, url):
        """
        rest call to the splunk rest-endpoint
            :param url: url to call
            :returns : json result of the request
        """
        res = requests.get(url, auth=(self.username, self.password), verify=False)
        assert res.status_code == 200, "url={}, status_code={}, error_msg={}".format(url,res.status_code, res.text)
        return res.json()
    
    def rest_call_post(self, url, kwargs):
        """
        rest call to the splunk rest-endpoint
            :param url: url to call
            :returns : json result of the request

            :param kwargs: body of request method
            :returns : json result of the request
        """
        res = requests.post(url, kwargs, auth=(self.username, self.password), verify=False)
        assert res.status_code == 200 or res.status_code == 201, "url={}, status_code={}, error_msg={}".format(url,res.status_code, res.text)
        return res.json()

    def rest_call_delete(self, url):
        """
        rest call to the splunk rest-endpoint
            :param url: url to call
            :returns : json result of the request
        """
        res = requests.delete(url, auth=(self.username, self.password), verify=False)
        assert res.status_code == 200 or res.status_code == 201, "url={}, status_code={}, error_msg={}".format(url,res.status_code, res.text)

    def parse_conf(self, json_res, single_stanza=False):
        """
        Parse the json result in to the configuration dictionary
            :param json_res: the json_res got from the request
            :returns : dictionary
        """
        stanzas_map = dict()
        for each_stanzas in json_res["entry"]:
            stanza_name = each_stanzas["name"]
            stanzas_map[stanza_name] = dict()

            for each_param, param_value in list(each_stanzas["content"].items()):                
                if each_param.startswith("eai:"):
                    continue
                stanzas_map[stanza_name][each_param] = param_value

        if single_stanza:
            return stanzas_map[list(stanzas_map.keys())[0]]
        return stanzas_map

class ListBackendConf(BackendConf):
    """
    For the configuration which can have more than one stanzas.
    The list will be fetched from endpoint/ and a specific stanza will be fetched from endpoint/{stanza_name}
    """

    def get_all_stanzas(self, query=None):
        """
        Get list of all stanzas of the configuration
            :query: query params for filter the stanza
            :returns : dictionary {stanza: {param: value, ... }, ... }
        """
        url = self.url + "?count=0&output_mode=json"
        if query:
            url = url + "&" + query
        res = self.rest_call(url)
        return self.parse_conf(res)


    def get_stanza(self, stanza, decrypt=False):
        """
        Get a specific stanza of the configuration.
            :param stanza: stanza to fetch
            :returns : dictionary {param: value, ... }
        """
        url = "{}/{}?count=0&output_mode=json".format(self.url, urllib.parse.quote_plus(stanza))
        if decrypt:
            url = "{}&--cred--=1".format(url)
        res = self.rest_call(url)
        return self.parse_conf(res, single_stanza=True)
    
    def post_stanza(self, url, kwargs):
        """
        Create a specific stanza of the configuration.
            :param url: url to call
            :returns : json result of the request

            :param kwargs: body of request method
            :returns : json result of the request
        """
        kwargs['output_mode'] = 'json'
        return self.rest_call_post(url, kwargs)

    def delete_all_stanzas(self, query=None):
        """
        Delete all stanza from the configuration.
            :query: query params for filter the stanza
            :returns : json result of the request
        """
        all_stanzas = list(self.get_all_stanzas(query).keys())
        for stanza in all_stanzas:
            self.delete_stanza(stanza)

    def delete_stanza(self, stanza):
        """
        Delete a specific stanza of the configuration.
            :param stanza: stanza to delete
            :returns : json result of the request
        """
        url = "{}/{}".format(self.url, urllib.parse.quote_plus(stanza))
        self.rest_call_delete(url)

    def get_stanza_value(self, stanza, param, decrypt=False):
        """
        Get value of a specific parameter from a stanza
            :param
        """
        stanza_map = self.get_stanza(stanza, decrypt)
        return stanza_map[param]

class SingleBackendConf(BackendConf):
    """
    For the configurations which can only have one stanza. for example, logging.
    """

    def get_stanza(self, decrypt=False):
        url = self.url + "?output_mode=json"
        if decrypt:
            url = "{}&--cred--=1".format(url)
        res = self.rest_call(url)
        return self.parse_conf(res, single_stanza=True)

    def get_parameter(self, param, decrypt=False):
        """
        Get value of a specific parameter from the stanza
            :param param: the parameter to fetch
        """
        stanza_map = self.get_stanza(decrypt)
        return stanza_map[param]
    
    def update_parameters(self, kwargs):
        kwargs['output_mode'] = 'json'
        return self.rest_call_post(self.url, kwargs)

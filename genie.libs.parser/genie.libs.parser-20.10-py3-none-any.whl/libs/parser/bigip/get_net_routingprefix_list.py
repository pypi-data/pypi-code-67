# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/net/routing/prefix-list' resources
# =============================================


class NetRoutingPrefixlistSchema(MetaParser):

    schema = {}


class NetRoutingPrefixlist(NetRoutingPrefixlistSchema):
    """ To F5 resource for /mgmt/tm/net/routing/prefix-list
    """

    cli_command = "/mgmt/tm/net/routing/prefix-list"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json

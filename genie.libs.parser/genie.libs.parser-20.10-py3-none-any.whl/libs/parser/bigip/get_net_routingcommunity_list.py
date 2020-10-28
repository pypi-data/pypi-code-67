# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/net/routing/community-list' resources
# =============================================


class NetRoutingCommunitylistSchema(MetaParser):

    schema = {}


class NetRoutingCommunitylist(NetRoutingCommunitylistSchema):
    """ To F5 resource for /mgmt/tm/net/routing/community-list
    """

    cli_command = "/mgmt/tm/net/routing/community-list"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json

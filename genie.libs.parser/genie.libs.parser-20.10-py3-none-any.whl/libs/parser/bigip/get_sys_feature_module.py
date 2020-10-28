# Global Imports
import json
from collections import defaultdict

# Metaparser
from genie.metaparser import MetaParser

# =============================================
# Collection for '/mgmt/tm/sys/feature-module' resources
# =============================================


class SysFeaturemoduleSchema(MetaParser):

    schema = {}


class SysFeaturemodule(SysFeaturemoduleSchema):
    """ To F5 resource for /mgmt/tm/sys/feature-module
    """

    cli_command = "/mgmt/tm/sys/feature-module"

    def rest(self):

        response = self.device.get(self.cli_command)

        response_json = response.json()

        if not response_json:
            return {}

        return response_json

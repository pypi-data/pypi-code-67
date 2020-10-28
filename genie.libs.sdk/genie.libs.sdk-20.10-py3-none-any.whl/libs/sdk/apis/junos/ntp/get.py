'''Common get info functions for ntp'''
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def get_ntp_peer_information(device, expected_mode=None):
    """ Get ntp peer information

        Args:
            device (`obj`): Device object
            expected_mode(`str`, Optional): Expected ntp mode. Defaults to None.
        Returns:
            result (`list`): List of peers
        Raises:
            N/A
    """
    peer_list = []
    try:
        output = device.parse('show ntp associations')
    except SchemaEmptyParserError:
        return peer_list

    # Example output
    # 'peer': {
    #     Any(): {
    #         'local_mode': {
    #             Any(): {
    #                 'remote': str,
    #                 'mode': str,

    if expected_mode:
        peer_list = Dq(output.q.contains_key_value('mode', expected_mode).reconstruct()).get_values('peer')
    else:
        peer_list = output.q.get_values('peer')
    return peer_list


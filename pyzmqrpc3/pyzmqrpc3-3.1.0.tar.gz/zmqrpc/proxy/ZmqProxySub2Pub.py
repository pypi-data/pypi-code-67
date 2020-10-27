

'''
Created on Apr 2014
Edited on Oct 2020

@author: Jan Verhoeven
@author: Bassem Girgis

@copyright: MIT license, see http://opensource.org/licenses/MIT
'''


from typing import Optional, Tuple

from ..receiver import SubSocketAddress
from .ZmqProxy import ZmqProxy


class ZmqProxySub2Pub(ZmqProxy):
    '''
    This class implements a simple message forwarding from a PUB/SUB connection
    to another PUB/SUB connection.
    Could be used to aggregate messages into one end-point.
    Note, at the moment username/password only protects the REQ-REP socket
    connection
    '''

    def __init__(
            self,
            zmq_sub_connect_addresses: Tuple[SubSocketAddress, ...],
            zmq_pub_bind_address: str,
            recreate_timeout: Optional[int] = 600,
            proxy_timeout: Optional[int] = 60,
            username_sub: Optional[str] = None,
            password_sub: Optional[str] = None,
            username_pub: Optional[str] = None,
            password_pub: Optional[str] = None):
        super().__init__(
            recv_sub_connect_addresses=zmq_sub_connect_addresses,
            recv_recreate_timeout=recreate_timeout,
            recv_username=username_sub,
            recv_password=password_sub,
            proxy_timeout=proxy_timeout,
            send_pub_endpoint=zmq_pub_bind_address,
            send_username=username_pub,
            send_password=password_pub,
        )

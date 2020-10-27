#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Komal Thareja (kthare10@renci.org)
from fabric.actor.core.apis.i_authority_proxy import IAuthorityProxy
from fabric.actor.core.apis.i_callback_proxy import ICallbackProxy
from fabric.actor.core.apis.i_client_callback_proxy import IClientCallbackProxy
from fabric.actor.core.apis.i_controller_callback_proxy import IControllerCallbackProxy
from fabric.actor.core.apis.i_controller_reservation import IControllerReservation
from fabric.actor.core.apis.i_rpc_request_state import IRPCRequestState
from fabric.actor.core.apis.i_reservation import IReservation
from fabric.actor.security.auth_token import AuthToken
from fabric.actor.test.dummy_proxy import DummyProxy


class DummyAuthorityProxy(DummyProxy, IAuthorityProxy):
    def __init__(self, *, auth: AuthToken = None):
        super().__init__(auth)

    def prepare_redeem(self, *, reservation: IControllerReservation, callback: IControllerCallbackProxy, caller:
    AuthToken) -> IRPCRequestState:
        return None

    def prepare_extend_lease(self, *, reservation: IControllerReservation, callback: IControllerCallbackProxy,
                             caller: AuthToken) -> IRPCRequestState:
        return None

    def prepare_modify_lease(self, *, reservation: IControllerReservation, callback: IControllerCallbackProxy,
                             caller: AuthToken) -> IRPCRequestState:
        return None

    def prepare_close(self, *, reservation: IControllerReservation, callback: IControllerCallbackProxy,
                      caller: AuthToken) -> IRPCRequestState:
        return None

    def prepare_ticket(self, *, reservation: IReservation, callback: IClientCallbackProxy, caller: AuthToken) -> IRPCRequestState:
        return None

    def prepare_claim(self, *, reservation: IReservation, callback: IClientCallbackProxy, caller: AuthToken) -> IRPCRequestState:
        return None

    def prepare_reclaim(self, *, reservation: IReservation, callback: IClientCallbackProxy, caller: AuthToken) -> IRPCRequestState:
        return None

    def prepare_extend_ticket(self, *, reservation: IReservation, callback: IClientCallbackProxy, caller: AuthToken) -> IRPCRequestState:
        return None

    def prepare_relinquish(self, *, reservation: IReservation, callback: IClientCallbackProxy, caller: AuthToken) -> IRPCRequestState:
        return None

    def prepare_query(self, *, callback: ICallbackProxy, query:dict, caller: AuthToken):
        return None
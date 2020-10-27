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
from __future__ import annotations
from typing import TYPE_CHECKING

from fabric.actor.core.apis.i_controller_callback_proxy import IControllerCallbackProxy
from fabric.actor.core.apis.i_delegation import IDelegation
from fabric.actor.core.common.constants import Constants
from fabric.actor.core.kernel.rpc_request_type import RPCRequestType
from fabric.actor.core.proxies.kafka.kafka_proxy import KafkaProxy, KafkaProxyRequestState
from fabric.actor.core.proxies.kafka.translate import Translate
from fabric.message_bus.messages.delegation_avro import DelegationAvro
from fabric.message_bus.messages.reservation_avro import ReservationAvro
from fabric.message_bus.messages.update_delegation_avro import UpdateDelegationAvro
from fabric.message_bus.messages.update_lease_avro import UpdateLeaseAvro
from fabric.message_bus.messages.update_ticket_avro import UpdateTicketAvro

if TYPE_CHECKING:
    from fabric.actor.security.auth_token import AuthToken
    from fabric.actor.core.apis.i_rpc_request_state import IRPCRequestState
    from fabric.actor.core.apis.i_broker_reservation import IBrokerReservation
    from fabric.actor.core.apis.i_callback_proxy import ICallbackProxy
    from fabric.actor.core.apis.i_authority_reservation import IAuthorityReservation
    from fabric.actor.core.apis.i_server_reservation import IServerReservation
    from fabric.actor.core.util.update_data import UpdateData


class KafkaReturn(KafkaProxy, IControllerCallbackProxy):
    def __init__(self, *, kafka_topic: str, identity: AuthToken, logger):
        super().__init__(kafka_topic=kafka_topic, identity=identity, logger=logger)
        self.type = KafkaProxy.TypeReturn
        self.callback = True

    def execute(self, *, request: IRPCRequestState):
        avro_message = None
        if request.get_type() == RPCRequestType.UpdateTicket:
            avro_message = UpdateTicketAvro()
            avro_message.message_id = str(request.get_message_id())
            avro_message.reservation = request.reservation
            avro_message.callback_topic = request.callback_topic
            avro_message.update_data = request.udd
            avro_message.auth = Translate.translate_auth_to_avro(auth=request.caller)

        elif request.get_type() == RPCRequestType.UpdateLease:
            avro_message = UpdateLeaseAvro()
            avro_message.message_id = str(request.get_message_id())
            avro_message.reservation = request.reservation
            avro_message.callback_topic = request.callback_topic
            avro_message.update_data = request.udd
            avro_message.auth = Translate.translate_auth_to_avro(auth=request.caller)

        elif request.get_type() == RPCRequestType.UpdateDelegation:
            avro_message = UpdateDelegationAvro()
            avro_message.message_id = str(request.get_message_id())
            avro_message.delegation = request.delegation
            avro_message.callback_topic = request.callback_topic
            avro_message.update_data = request.udd
            avro_message.auth = Translate.translate_auth_to_avro(auth=request.caller)

        else:
            return super().execute(request=request)

        if self.producer is None:
            self.producer = self.create_kafka_producer()

        if self.producer is not None and self.producer.produce_sync(topic=self.kafka_topic, record=avro_message):
            self.logger.debug("Message {} written to {}".format(avro_message.name, self.kafka_topic))
        else:
            self.logger.error("Failed to send message {} to {} via producer {}".format(avro_message.name,
                                                                                       self.kafka_topic, self.producer))

    def prepare_update_ticket(self, *, reservation: IBrokerReservation, update_data: UpdateData,
                              callback: ICallbackProxy, caller: AuthToken) -> IRPCRequestState:
        request = KafkaProxyRequestState()
        request.reservation = self.pass_reservation(reservation=reservation, auth=caller)
        request.udd = Translate.translate_udd(udd=update_data)
        request.callback_topic = callback.get_kafka_topic()
        request.caller = caller
        return request

    def prepare_update_delegation(self, *, delegation: IDelegation, update_data: UpdateData,
                                  callback: ICallbackProxy, caller: AuthToken) -> IRPCRequestState:
        request = KafkaProxyRequestState()
        request.delegation = self.pass_delegation(delegation=delegation, auth=caller)
        request.udd = Translate.translate_udd(udd=update_data)
        request.callback_topic = callback.get_kafka_topic()
        request.caller = caller
        return request

    def prepare_update_lease(self, *, reservation: IAuthorityReservation,  update_data: UpdateData,
                             callback: ICallbackProxy, caller: AuthToken) -> IRPCRequestState:
        request = KafkaProxyRequestState()
        request.reservation = self.pass_reservation(reservation=reservation, auth=caller)
        request.udd = Translate.translate_udd(udd=update_data)
        request.callback_topic = callback.get_kafka_topic()
        request.caller = caller
        return request

    @staticmethod
    def pass_reservation(reservation: IServerReservation, auth: AuthToken) -> ReservationAvro:
        avro_reservation = ReservationAvro()
        avro_reservation.slice = Translate.translate_slice_to_avro(slice_obj=reservation.get_slice())
        term = None
        if reservation.get_term() is None:
            term = reservation.get_requested_term().clone()
        else:
            term = reservation.get_term().clone()

        avro_reservation.term = Translate.translate_term(term=term)
        avro_reservation.reservation_id = str(reservation.get_reservation_id())

        rset = None
        if reservation.get_resources() is None:
            from fabric.actor.core.kernel.resource_set import ResourceSet
            from fabric.actor.core.util.resource_data import ResourceData
            rset = Translate.translate_resource_set(resource_set=ResourceSet(units=0,
                                                                             rtype=reservation.get_requested_type(),
                                                                             rdata=ResourceData()),
                                                    direction=Translate.DirectionReturn)
        else:
            rset = Translate.translate_resource_set(resource_set=reservation.get_resources(),
                                                    direction=Translate.DirectionReturn)

        cset = reservation.get_resources().get_resources()

        encoded = None
        if cset is not None:
            encoded = cset.encode(protocol=Constants.ProtocolKafka)
            if encoded is None:
                raise Exception("Unsupported IConcreteSet: {}".format(type(cset)))

        rset.concrete = encoded

        avro_reservation.resource_set = rset
        return avro_reservation

    @staticmethod
    def pass_delegation(delegation: IDelegation, auth: AuthToken) -> DelegationAvro:
        avro_delegation = Translate.translate_delegation_to_avro(delegation=delegation)
        avro_delegation.sequence = delegation.get_sequence_out()
        return avro_delegation

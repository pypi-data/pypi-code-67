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

from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, List

from fabric.actor.core.apis.i_component import IComponent
from fabric.message_bus.messages.pool_info_avro import PoolInfoAvro

if TYPE_CHECKING:
    from fabric.message_bus.messages.ticket_reservation_avro import TicketReservationAvro
    from fabric.actor.core.util.id import ID
    from fabric.message_bus.messages.reservation_mng import ReservationMng
    from fabric.message_bus.messages.proxy_avro import ProxyAvro
    from fabric.actor.core.util.resource_type import ResourceType


class IMgmtClientActor(IComponent):
    @abstractmethod
    def add_reservation(self, *, reservation: TicketReservationAvro) -> ID:
        """
        Adds the reservation to the actor's state and returns the assigned reservation ID.
        The reservation must refer to a valid slice.
        The reservation ID is also attached to the passed in reservation object.
        @param reservation reservation
        @return null on failure, assigned reservation ID otherwise
        """

    @abstractmethod
    def add_reservations(self, *, reservations: List[ReservationMng])->list:
        """
        Adds all reservations to the actor's state and returns the assigned reservation ID.
        Each reservation must refer to a valid slice.
        The reservation ID is also attached to the passed in reservation object.
        The operation is atomic: all of the reservations are added or none of them is added.
        @param reservations reservation
        @return null on failure, list of assigned ReservationIDs on success.
        """

    @abstractmethod
    def demand_reservation_rid(self, *, rid: ID) -> bool:
        """
        Demands the specified reservation.
        A reservation can be demanded only if has been added and it is in the Nascent state.
        @param rid reservation id
        @return true for success; false otherwise
        """

    @abstractmethod
    def demand_reservation(self, *, reservation: ReservationMng) -> bool:
        """
        Updates the reservation and issues a demand for it.
        A reservation can be demanded only if has been added and it is in the Nascent state.
        The reservation must refer to a valid slice. It can also indicate
        redeem predecessors.
        @param reservation reservation
        @return true for success; false otherwise
        """

    @abstractmethod
    def get_brokers(self) -> List[ProxyAvro]:
        """
        Retuns all brokers known to the actor.
        @return list of all brokers
        """

    @abstractmethod
    def get_broker(self, *, broker: ID) -> ProxyAvro:
        """
        Returns the broker with the specified ID.
        @param broker broker id
        @return returns specified broker
        """

    @abstractmethod
    def add_broker(self, *, broker: ProxyAvro) -> bool:
        """
        Adds a new broker.
        @param broker broker
        @return true for sucess; false otherwise
        """

    @abstractmethod
    def get_pool_info(self, *, broker: ID) -> List[PoolInfoAvro]:
        """
        Obtains the resources available at the specified broker
        @param broker broker
        @return list of pool info
        """

    @abstractmethod
    def claim_resources_slice(self, *, broker: ID, slice_id: ID, rid: ID) -> ReservationMng:
        """
        Claims resources exported by the specified broker
        @param broker broker guid
        @param slice_id slice id
        @param rid reservation id
        @return reservation
        """

    @abstractmethod
    def claim_resources(self, *, broker: ID, rid: ID) -> ReservationMng:
        """
        Claims resources exported by the specified broker
        @param broker broker guid
        @param rid reservation id
        @return reservation
        """

    @abstractmethod
    def extend_reservation(self, *, reservation: ID, new_end_time: datetime, new_units: int,
                           new_resource_type: ResourceType, request_properties: dict,
                           config_properties: dict) -> bool:
        """
        Extend a reservation
        @params reservation: reservation id
        @params new_end_time: new end time
        @params new_units: new_units
        @params new_resource_type: new_resource_type
        @params request_properties: request_properties
        @params config_properties: config_properties
        @return true for success and false for failure
        """

    @abstractmethod
    def extend_reservation_end_time(self, *, reservation: ID, new_end_time: datetime) -> bool:
        """
        Extend a reservation
        @params reservation: reservation id
        @params new_end_time: new end time
        @return true for success and false for failure
        """

    @abstractmethod
    def extend_reservation_end_time_request(self, *, reservation: ID, new_end_time: datetime,
                                            request_properties: dict) -> bool:
        """
        Extend a reservation
        @params reservation: reservation id
        @params new_end_time: new end time
        @params request_properties: request_properties
        @return true for success and false for failure
        """

    @abstractmethod
    def extend_reservation_end_time_request_config(self, *, reservation: ID, new_end_time: datetime,
                                                   request_properties: dict, config_properties: dict) -> bool:
        """
        Extend a reservation
        @params reservation: reservation id
        @params new_end_time: new end time
        @params request_properties: request_properties
        @params config_properties: config_properties
        @return true for success and false for failure
        """

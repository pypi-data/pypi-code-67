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

from fabric.actor.core.util.id import ID

if TYPE_CHECKING:
    from fabric.actor.security.auth_token import AuthToken
    from fabric.actor.core.apis.i_event_filter import IEventFilter
    from fabric.actor.core.apis.i_event import IEvent


class AEventSubscription:
    def __init__(self, *, token: AuthToken, filters: list):
        self.subscription_id = ID()
        self.token = token
        self.filters = {}
        for f in filters:
            self.filters[ID()] = f

    def get_subscription_id(self):
        return self.subscription_id

    def has_access(self, *, token: AuthToken) -> bool:
        if token is None:
            return False
        if token.get_name() is None:
            return False
        if self.token is None:
            return False
        return self.token.get_name() == token.get_name()

    def add_event_filter(self, *, f: IEventFilter):
        fid = ID()
        self.filters[fid] = f

    def delete_filter(self, *, fid: ID):
        if fid in self.filters:
            self.filters.pop(fid)

    def matches(self, *, event: IEvent):
        if len(self.filters) == 0:
            return True
        for f in self.filters.values():
            if not f.matches(event=event):
                return False
        return True

    def deliver_event(self, *, event: IEvent):
        raise NotImplementedError("Should have implemented this")

    def drain_events(self, *, timeout: int) -> list:
        raise NotImplementedError("Should have implemented this")

    def is_abandoned(self) -> bool:
        raise NotImplementedError("Should have implemented this")
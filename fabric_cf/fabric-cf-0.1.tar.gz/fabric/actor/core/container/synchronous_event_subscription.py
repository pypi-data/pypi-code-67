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

from fabric.actor.core.container.aevent_subscription import AEventSubscription

if TYPE_CHECKING:
    from fabric.actor.core.apis.i_event_handler import IEventHandler
    from fabric.actor.security.auth_token import AuthToken
    from fabric.actor.core.apis.i_event import IEvent


class SynchronousEventSubscription(AEventSubscription):
    def __init__(self, *, handler: IEventHandler, token: AuthToken, filters: list):
        super().__init__(token=token, filters=filters)
        self.handler = handler

    def deliver_event(self, *, event: IEvent):
        if self.matches(event=event):
            self.handler.handle(event=event)

    def drain_events(self, *, timeout: int) -> list:
        raise Exception("drainEvents is not supported on synchronous subscriptions")

    def is_abandoned(self) -> bool:
        return False

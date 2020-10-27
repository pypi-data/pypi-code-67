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
import unittest
import time
from fabric.actor.core.apis.i_container_database import IContainerDatabase
from fabric.actor.core.common.constants import Constants
from fabric.actor.test.base_test_case import BaseTestCase


class ContainerDatabaseTest(BaseTestCase, unittest.TestCase):
    from fabric.actor.core.container.globals import Globals
    Globals.ConfigFile = Constants.TestVmAmConfigurationFile

    from fabric.actor.core.container.globals import GlobalsSingleton
    GlobalsSingleton.get().start(force_fresh=True)
    while not GlobalsSingleton.get().start_completed:
        time.sleep(0.0001)

    container = GlobalsSingleton.get().get_container()

    def get_clean_database(self) -> IContainerDatabase:
        self.db = self.container.get_database()
        return self.db

    def test_a_create(self):
        db = self.get_clean_database()
        self.assertEqual(1, len(db.get_actors()), "No actors")
        self.assertIsNone(db.get_container_properties())
        self.assertIsNotNone(db.get_time())

    def test_b_add_remove_actor(self):
        db = self.get_clean_database()

        actor = self.get_actor()

        result = db.get_actor(actor_name=self.ActorName)
        self.assertIsNotNone(result)

        result = db.get_actors()

        self.assertIsNotNone(result)
        self.assertEqual(2, len(result), "Two actor")

        db.remove_actor(actor_name=self.ActorName)

        self.assertIsNone(db.get_actor(actor_name=self.ActorName))

        self.assertEqual(1, len(db.get_actors()), "One actor")

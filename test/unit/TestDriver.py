# Copyright 2015 Spotify AB. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import unittest

from lxml import etree
from napalm_sros.sros import NokiaSROSDriver
from napalm.base.test.base import TestConfigNetworkDriver, TestGettersNetworkDriver


class TestConfigNokiaSROSDriver(unittest.TestCase, TestConfigNetworkDriver):
    @classmethod
    def setUpClass(cls):
        hostname = "127.0.0.1"
        username = "vagrant"
        password = "vagrant"
        cls.vendor = "sros"

        optional_args = {"port": 830}
        cls.device = NokiaSROSDriver(
            hostname, username, password, timeout=60, optional_args=optional_args
        )
        cls.device.open()


method_name = None


class TestGetterNokiaSROSDriver(unittest.TestCase, TestGettersNetworkDriver):
    def setUp(self):
        global method_name
        method_name = self._testMethodName

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock = True
        hostname = "192.168.56.203"
        username = "vagrant"
        password = "vagrant123"
        cls.vendor = "sros"
        optional_args = {}
        cls.device = NokiaSROSDriver(
            hostname, username, password, timeout=60, optional_args=optional_args
        )

        if cls.mock:
            cls.device.conn_ssh = FakeSSHConnection()
            cls.device.ssh_channel = FakeSSHConnectionChannel()
            cls.device.conn = FakeNokiaSROSDevice()
        else:
            cls.device.open()

    @staticmethod
    def read_txt_file(filename):
        with open(filename) as data_file:
            return data_file.read()


class FakeSSHConnection:
    def __init__(self):
        self.get_transport = FakeGetTransport


class FakeGetTransport:
    @staticmethod
    def is_active():
        return True


class FakeSSHConnectionChannel:
    def __init__(self):
        self.command = ""
        self.buff = ""

    def send(self, c=""):
        self.command = c

    def recv(self, byte):
        command_list = self.command.split("\n")
        command = command_list[0].replace(" ", "_")
        if "." in command:
            command = command.replace(".", "_")
        if "|" in command:
            command = command.replace("|", "_")
        if "/" in command:
            command = command.replace("/", "_")
        response_string = TestGetterNokiaSROSDriver.read_txt_file(
            "sros/mock_data/{}.txt".format(command)
        )
        response_string = response_string.ljust(len(response_string) + 1, " ")
        return str.encode(response_string)


class FakeNokiaSROSDevice:
    def __init__(self):
        self.get = FakeGetMethod()

    def open(self):
        pass

    def close(self):
        pass


class FakeGetMethod:
    """
    Fake Get Method.
    """

    def response(self, filter="", with_defaults=""):
        file_name = method_name
        file_name = file_name.split("_", 1)[1]

        response_string = TestGetterNokiaSROSDriver.read_txt_file(
            "sros/mock_data/{}.txt".format(file_name)
        )

        return FakeGetReply(data=response_string)
    __call__ = response


class FakeGetReply:
    """
    Will fake the GetReply class of ncclient
    """

    def __init__(self, data):
        self._data = data

    @property
    def data_xml(self):
        return to_ele(etree.fromstring(self._data.encode("UTF-8")))


def to_ele(x):
    return x if etree.iselement(x) else etree.fromstring(x.encode("UTF-8"))

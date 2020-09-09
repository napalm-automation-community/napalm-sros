"""Test fixtures."""

import pytest
from lxml import etree

from napalm.base.test import conftest as parent_conftest
# from ncclient import manager
from napalm.base.test.double import BaseTestDouble

from napalm_sros import sros


@pytest.fixture(scope="class")
def set_device_parameters(request):
    """Set up the class."""

    def fin():
        request.cls.device.close()

    request.addfinalizer(fin)

    request.cls.driver = sros.NokiaSROSDriver
    request.cls.patched_driver = PatchedNokiaSROSDriver
    request.cls.vendor = "sros"
    parent_conftest.set_device_parameters(request)


def pytest_generate_tests(metafunc):
    """Generate test cases dynamically."""
    parent_conftest.pytest_generate_tests(metafunc, __file__)


class PatchedNokiaSROSDriver(sros.NokiaSROSDriver):
    """Patched NokiaSROS Driver."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):

        super(self.__class__, self).__init__(
            hostname, username, password, timeout, optional_args=optional_args
        )

        self.patched_attrs = ["conn", "ssh_channel"]
        self.conn = FakeNokiaSROSDevice()
        self.ssh_channel = FakeSSHConnectionChannel()
        self.conn_ssh = FakeSSHConnection()
        self.manager = FakeManager()

    def is_alive(self):
        return {"is_alive": True}



class FakeNokiaSROSDevice(BaseTestDouble):
    def __init__(self):
        self.get = FakeGetMethod(self)

    def close_session(self):
        pass


class FakeManager:
    """
    Fake ncclient manager class"
    """

    def __init__(self):
        self.conn = FakeNokiaSROSDevice()

    def connect(self):
        return self.conn


class FakeGetMethod:
    """
    Fake Get Method.
    """
    def __init__(self, device):
        self._device = device

    def response(self, filter="", with_defaults=""):
        test_name = self._device.current_test
        filename = "{}.xml".format(test_name.split("_", 1)[1])
        filepath = self._device.find_file(filename)
        response_string = self._device.read_txt_file(filepath)

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


class FakeSSHConnection:
    def __init__(self):
        self.get_transport = FakeGetTransport


class FakeGetTransport:
    @staticmethod
    def is_active():
        return True


class FakeSSHConnectionChannel(BaseTestDouble):
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
        filename = "{}.txt".format(command)
        filepath = self.find_file(filename)
        response_string = self.read_txt_file(filepath)
        response_string = response_string.ljust(len(response_string) + 1, " ")
        return str.encode(response_string)



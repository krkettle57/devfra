import io
import textwrap
from ipaddress import IPv4Network
from typing import IO

from loader import load_config
from models.devfra import DevfraBastionConfig, DevfraConfig, DevfraInstanceConfig, DevfraNetworkConfig
from pytest import fixture


@fixture
def file_only_users() -> IO:
    yaml_str = textwrap.dedent(
        """
        prefix: test
        instances:
        - name: user1
        - name: user2
        """
    )
    return io.StringIO(yaml_str)


def test_load_config(file_only_users):
    actual = load_config(file_only_users)
    expected = DevfraConfig(
        prefix="test",
        source_cidr_list=[IPv4Network("0.0.0.0/0")],
        network=DevfraNetworkConfig(),
        bastion=DevfraBastionConfig(),
        instances=[
            DevfraInstanceConfig(name="user1"),
            DevfraInstanceConfig(name="user2"),
        ],
    )
    assert actual == expected

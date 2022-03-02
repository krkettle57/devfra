from ipaddress import IPv4Address, IPv4Network

import pytest
from network import PrivateIPAllocator


class TestPrivateIPAllocator:
    def test_allocate_first(self):
        sbn_cidr = IPv4Network("10.0.0.0/24")
        allocator = PrivateIPAllocator(sbn_cidr)
        expected = IPv4Address("10.0.0.4")
        assert allocator.allocate() == expected

    def test_allocate_last(self):
        sbn_cidr = IPv4Network("10.0.0.0/29")
        allocator = PrivateIPAllocator(sbn_cidr)

        # allocate 10.0.0.4/32 - 10.0.0.6/32
        for _ in range(3):
            allocator.allocate()

        # 10.0.0.7/32 is allocated for AWS
        with pytest.raises(Exception):
            allocator.allocate()

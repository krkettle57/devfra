from ipaddress import AddressValueError, IPv4Address, IPv4Network
from typing import Any

from pydantic import BaseModel, PrivateAttr

from exceptions import DevfraError


class PrivateIPAllocator(BaseModel):
    sbn_cidr: IPv4Network
    __max_allocated_addr: IPv4Address = PrivateAttr()

    def __init__(self, sbn_cidr: IPv4Network, **data: Any) -> None:
        data["sbn_cidr"] = sbn_cidr
        # first 4 ips are allocated by AWS
        # Ref: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-sizing-ipv4
        self.__max_allocated_addr = sbn_cidr[3]
        super().__init__(**data)

    def allocate(self) -> IPv4Address:
        # last ip is allocated by AWS
        # Ref: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-sizing-ipv4
        if self.__max_allocated_addr == self.sbn_cidr[-2]:
            raise DevfraError("No allocatable ip.")
        self.__max_allocated_addr += 1
        return self.__max_allocated_addr


def str2ipv4network(key: str, value: str) -> IPv4Network:
    try:
        network = IPv4Network(value)
    except AddressValueError:
        raise DevfraError(f"{key} is invalid value.")

    return network

from ipaddress import IPv4Network
from pathlib import Path
from typing import List, Optional

from deufalt import (
    DEFAULT_AMI_ID,
    DEFAULT_INSTANCE_TYPE,
    DEFAULT_PRIVATE_SUBNET_VPC_CIDR,
    DEFAULT_PUBLIC_SUBNET_CIDR,
    DEFAULT_VPC_CIDR,
)
from pydantic import BaseModel


class DevfraNetworkConfig(BaseModel):
    vpc_cidr: IPv4Network = DEFAULT_VPC_CIDR
    public_subnet_cidr: IPv4Network = DEFAULT_PUBLIC_SUBNET_CIDR
    private_subnet_cidr: IPv4Network = DEFAULT_PRIVATE_SUBNET_VPC_CIDR


class DevfraBastionConfig(BaseModel):
    name = "bastion"
    public_keypath: Optional[Path] = None
    private_keypath: Optional[Path] = None
    ami_id: str = DEFAULT_AMI_ID
    instance_type: str = DEFAULT_INSTANCE_TYPE


class DevfraInstanceConfig(BaseModel):
    name: str
    public_keypath: Optional[Path] = None
    private_keypath: Optional[Path] = None
    ami_id: str = DEFAULT_AMI_ID
    instance_type: str = DEFAULT_INSTANCE_TYPE


class DevfraConfig(BaseModel):
    prefix: str
    source_cidr_list: List[IPv4Network]
    network: DevfraNetworkConfig
    bastion: DevfraBastionConfig
    instances: List[DevfraInstanceConfig]

from ipaddress import IPv4Address, IPv4Network
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel


class TFVarNetworkConfig(BaseModel):
    vpc_cidr: IPv4Network
    public_subnet_cidr: IPv4Network
    private_subnet_cidr: IPv4Network


class TFVarBastionConfig(BaseModel):
    public_keypath: Path
    private_keypath: Path
    ami_id: str
    instance_type: str


class TFVarInstaceConfig(BaseModel):
    name: str
    public_keypath: Path
    private_keypath: Optional[Path]
    ami_id: str
    instance_type: str
    private_ip: IPv4Address


# The reason that source_cidr_list isn't the field of TFVarBastionConfig
#  Terraform map variable must have all the same element.
class TFVarConfig(BaseModel):
    prefix: str
    network: TFVarNetworkConfig
    bastion: TFVarBastionConfig
    instances: Dict[str, TFVarInstaceConfig]
    source_cidr_list: List[IPv4Network]

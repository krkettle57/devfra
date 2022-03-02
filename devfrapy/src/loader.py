from ipaddress import IPv4Network
from typing import IO, Dict, List

import yaml

from exceptions import DevfraError
from models.devfra import DevfraBastionConfig, DevfraConfig, DevfraInstanceConfig, DevfraNetworkConfig


def load_network_config(network: Dict) -> DevfraNetworkConfig:
    # TODO: validation
    devfra_network = DevfraNetworkConfig(**network)
    return devfra_network


def load_bastion_config(bastion: Dict) -> DevfraBastionConfig:
    # TODO: validation
    devfra_bastion = DevfraBastionConfig(**bastion)
    return devfra_bastion


def load_instances_config(instances: List[Dict]) -> List[DevfraInstanceConfig]:
    devfra_instances = []
    for instance in instances:
        if "name" not in instance:
            raise DevfraError("'instances[].name' is required.")

        # TODO: validation
        devfra_instance = DevfraInstanceConfig(**instance)
        devfra_instances.append(devfra_instance)

    return devfra_instances


def load_config(file: IO) -> DevfraConfig:
    raw = yaml.safe_load(file)

    # DevfraConfig fields
    if "prefix" in raw:
        prefix = raw["prefix"]
    else:
        raise DevfraError("'prefix' is required.")

    if "source_cidr_list" not in raw:
        source_cidr_list = [IPv4Network("0.0.0.0/0")]

    # DevfraNetwork
    devfra_network_config = DevfraNetworkConfig()
    if "network" in raw:
        devfra_network_config = load_network_config(raw["network"])

    # DevfraBastion
    devfra_bastion_config = DevfraBastionConfig()
    if "bastion" in raw:
        devfra_bastion_config = load_bastion_config(raw["bastion"])

    # DevfraInstances
    devfra_instances_config = []
    if "instances" in raw:
        devfra_instances_config = load_instances_config(raw["instances"])

    # TODO: validation
    devfra_config = DevfraConfig(
        prefix=prefix,
        source_cidr_list=source_cidr_list,
        network=devfra_network_config,
        bastion=devfra_bastion_config,
        instances=devfra_instances_config,
    )

    return devfra_config

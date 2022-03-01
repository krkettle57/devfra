from ipaddress import IPv4Network
from typing import IO, Dict, List

import yaml

from exceptions import DevfraError
from models.devfra import DevfraBastionConfig, DevfraConfig, DevfraInstanceConfig, DevfraNetworkConfig


def load_network_config(raw: Dict) -> DevfraNetworkConfig:
    if "network" not in raw:
        return DevfraNetworkConfig()

    # TODO: validation
    network = DevfraNetworkConfig(**raw["network"])

    return network


def load_bastion_config(raw: Dict) -> DevfraBastionConfig:
    if "bastion" not in raw:
        return DevfraBastionConfig()

    raw_bastion = raw["bastion"]

    # TODO: validation
    bastion = DevfraBastionConfig(**raw_bastion)

    return bastion


def load_instances_config(raw: Dict) -> List[DevfraInstanceConfig]:
    if "instances" not in raw:
        return []

    instances = []
    for raw_instance in raw["instances"]:
        if "name" not in raw_instance:
            raise DevfraError("'instances[].name' is required.")

        # TODO: validation
        instance = DevfraInstanceConfig(**raw_instance)
        instances.append(instance)

    return instances


def load_config(file: IO) -> DevfraConfig:
    raw = yaml.safe_load(file)

    if "prefix" in raw:
        prefix = raw["prefix"]
    else:
        raise DevfraError("'prefix' is required.")

    if "source_cidr_list" not in raw:
        source_cidr_list = [IPv4Network("0.0.0.0/0")]

    devfra_network_config = load_network_config(raw)
    devfra_bastion_config = load_bastion_config(raw)
    devfra_instances_config = load_instances_config(raw)
    devfra_config = DevfraConfig(
        prefix=prefix,
        network=devfra_network_config,
        bastion=devfra_bastion_config,
        instances=devfra_instances_config,
        source_cidr_list=source_cidr_list,
    )

    return devfra_config

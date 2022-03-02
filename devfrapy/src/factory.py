from typing import Tuple

from keypair import KeyPairRegistry
from models.devfra import DevfraBastionConfig, DevfraConfig, DevfraInstanceConfig, DevfraNetworkConfig
from models.tfvar import TFVarBastionConfig, TFVarConfig, TFVarInstaceConfig, TFVarNetworkConfig
from network import PrivateIPAllocator


def tfvar_network_factory(devfra_network_config: DevfraNetworkConfig) -> TFVarNetworkConfig:
    tfvar_network_config = TFVarNetworkConfig(
        vpc_cidr=devfra_network_config.vpc_cidr,
        public_subnet_cidr=devfra_network_config.public_subnet_cidr,
        private_subnet_cidr=devfra_network_config.private_subnet_cidr,
    )
    return tfvar_network_config


def tfvar_bastion_factory(
    devfra_bastion_config: DevfraBastionConfig, keypair_registry: KeyPairRegistry
) -> TFVarBastionConfig:
    private_keypath = devfra_bastion_config.private_keypath
    public_keypath = devfra_bastion_config.public_keypath
    if private_keypath is None or public_keypath is None:
        keypair_path = keypair_registry.register(name=devfra_bastion_config.name)
        private_keypath = keypair_path.private_keypath
        public_keypath = keypair_path.public_keypath

    tfvar_bastion_config = TFVarBastionConfig(
        public_keypath=public_keypath,
        private_keypath=private_keypath,
        ami_id=devfra_bastion_config.ami_id,
        instance_type=devfra_bastion_config.instance_type,
    )
    return tfvar_bastion_config


def tfvar_instance_factory(
    devfra_instance_config: DevfraInstanceConfig,
    private_ip_allocator: PrivateIPAllocator,
    keypair_registry: KeyPairRegistry,
) -> TFVarInstaceConfig:
    private_keypath = devfra_instance_config.private_keypath
    public_keypath = devfra_instance_config.public_keypath
    if public_keypath is None:
        keypair_path = keypair_registry.register(name=devfra_instance_config.name)
        private_keypath = keypair_path.private_keypath
        public_keypath = keypair_path.public_keypath

    private_ip = private_ip_allocator.allocate()
    tfvar_instance_config = TFVarInstaceConfig(
        name=devfra_instance_config.name,
        public_keypath=public_keypath,
        private_keypath=private_keypath,
        ami_id=devfra_instance_config.ami_id,
        instance_type=devfra_instance_config.instance_type,
        private_ip=private_ip,
    )
    return tfvar_instance_config


def tfvar_config_factory(
    devfra_config: DevfraConfig, keypair_registry: KeyPairRegistry
) -> Tuple[TFVarConfig, KeyPairRegistry]:
    private_ip_allocator = PrivateIPAllocator(devfra_config.network.private_subnet_cidr)
    tfv_network_config = tfvar_network_factory(devfra_config.network)
    tfv_bastion_config = tfvar_bastion_factory(devfra_config.bastion, keypair_registry)
    tfv_instances_config = {
        instance.name: tfvar_instance_factory(instance, private_ip_allocator, keypair_registry)
        for instance in devfra_config.instances
    }
    tfvar_config = TFVarConfig(
        prefix=devfra_config.prefix,
        source_cidr_list=devfra_config.source_cidr_list,
        network=tfv_network_config,
        bastion=tfv_bastion_config,
        instances=tfv_instances_config,
    )
    return tfvar_config, keypair_registry

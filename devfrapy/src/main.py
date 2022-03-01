import argparse
from pathlib import Path

from factory import tfvar_config_factory
from keypair import KeyPairGenerator, KeyPairRegistry
from loader import load_config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="The path of devfra yaml path.")
    parser.add_argument("working_dir", help="The path of working directory.")

    args = parser.parse_args()
    working_dir = Path(args.working_dir).resolve()

    # Load devfra models
    devfra_config = None
    with open(args.path) as f:
        devfra_config = load_config(f)

    # Create tfvar models
    keypair_generator = KeyPairGenerator()
    keypair_registry = KeyPairRegistry(
        keypair_generator=keypair_generator,
        working_dir=working_dir,
    )
    tfv_config, keypair_registry = tfvar_config_factory(
        devfra_config=devfra_config,
        keypair_registry=keypair_registry,
    )

    # write tfvar config
    tfv_config_path = Path(working_dir, "config/tfvar.json")
    tfv_config_path.parent.resolve().mkdir(parents=True, exist_ok=True)
    tfv_config_path.write_text(tfv_config.json())

    # write secrets
    for keypair_conf in keypair_registry.keypair_conf_list:
        private_path = keypair_conf.keypair_path.private_keypath
        if private_path is not None:
            private_path.parent.resolve().mkdir(parents=True, exist_ok=True)
            private_path.write_text(keypair_conf.keypair.private_key)

        public_path = keypair_conf.keypair_path.public_keypath
        public_path.parent.resolve().mkdir(parents=True, exist_ok=True)
        public_path.write_text(keypair_conf.keypair.public_key)

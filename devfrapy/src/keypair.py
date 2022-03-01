from pathlib import Path
from typing import List, Optional

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import BaseModel, PrivateAttr


class KeyPair(BaseModel):
    private_key: str
    public_key: str


class KeyPairPath(BaseModel):
    private_keypath: Optional[Path]
    public_keypath: Path


class KeyPairGenerator(BaseModel):
    keytype: str = "rsa"

    def generate(self) -> KeyPair:
        return self.rsa()

    def rsa(self, keysize: int = 4096, encoding: str = "utf-8") -> KeyPair:
        key = rsa.generate_private_key(public_exponent=65537, key_size=keysize)

        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.OpenSSH,
            crypto_serialization.NoEncryption(),
        )

        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH,
        )

        keypair = KeyPair(
            private_key=private_key.decode(encoding),
            public_key=public_key.decode(encoding),
        )
        return keypair


class KeyPairConf(BaseModel):
    name: str
    keypair: KeyPair
    keypair_path: KeyPairPath


class KeyPairRegistry(BaseModel):
    keypair_generator: KeyPairGenerator
    working_dir: Path
    __keypair_conf_list: List[KeyPairConf] = PrivateAttr(default_factory=list)

    def register(self, name: str) -> KeyPairPath:
        secret_dir = Path(self.working_dir, f"config/secrets/{name}")
        private_keypath = Path(secret_dir, "id_rsa")
        public_keypath = Path(secret_dir, "id_rsa.pub")
        keypair_path = KeyPairPath(
            private_keypath=private_keypath,
            public_keypath=public_keypath,
        )

        if private_keypath.exists() or public_keypath.exists():
            return keypair_path

        keypair = self.keypair_generator.generate()
        keypair_conf = KeyPairConf(name=name, keypair=keypair, keypair_path=keypair_path)
        self.__keypair_conf_list.append(keypair_conf)
        return keypair_path

    @property
    def keypair_conf_list(self) -> List[KeyPairConf]:
        return self.__keypair_conf_list

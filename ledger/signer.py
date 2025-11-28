from __future__ import annotations

import base64
from pathlib import Path
from typing import Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

KEY_DIR = Path.home() / ".aion" / "keys"
PRIVATE_KEY_PATH = KEY_DIR / "private.key"
PUBLIC_KEY_PATH = KEY_DIR / "public.key"


def _load_private_key() -> Ed25519PrivateKey:
    data = PRIVATE_KEY_PATH.read_bytes()
    return serialization.load_pem_private_key(data, password=None)


def _load_public_key() -> Ed25519PublicKey:
    data = PUBLIC_KEY_PATH.read_bytes()
    return serialization.load_pem_public_key(data)


def ensure_keys() -> Tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    KEY_DIR.mkdir(parents=True, exist_ok=True)

    if not PRIVATE_KEY_PATH.exists() or not PUBLIC_KEY_PATH.exists():
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        PRIVATE_KEY_PATH.write_bytes(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        PUBLIC_KEY_PATH.write_bytes(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
        return private_key, public_key

    return _load_private_key(), _load_public_key()


def sign(data: bytes) -> str:
    private_key, _ = ensure_keys()
    signature = private_key.sign(data)
    return base64.b64encode(signature).decode()


def verify_signature(data: bytes, signature_b64: str) -> bool:
    _, public_key = ensure_keys()
    signature = base64.b64decode(signature_b64)
    try:
        public_key.verify(signature, data)
        return True
    except Exception:
        return False

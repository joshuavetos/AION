import base64
from pathlib import Path
from typing import Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

KEY_DIR = Path.home() / ".aion" / "keys"
PRIVATE_KEY_PATH = KEY_DIR / "private.key"
PUBLIC_KEY_PATH = KEY_DIR / "public.key"


def _generate_keypair() -> Tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    KEY_DIR.mkdir(parents=True, exist_ok=True)
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


def _load_keys() -> Tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    if not PRIVATE_KEY_PATH.exists() or not PUBLIC_KEY_PATH.exists():
        return _generate_keypair()

    private_bytes = PRIVATE_KEY_PATH.read_bytes()
    public_bytes = PUBLIC_KEY_PATH.read_bytes()

    private_key = serialization.load_pem_private_key(private_bytes, password=None)
    public_key = serialization.load_pem_public_key(public_bytes)

    if not isinstance(private_key, Ed25519PrivateKey) or not isinstance(public_key, Ed25519PublicKey):
        raise ValueError("Invalid key types found in key storage")

    return private_key, public_key


def sign(data: bytes) -> str:
    private_key, _ = _load_keys()
    signature = private_key.sign(data)
    return base64.b64encode(signature).decode("utf-8")


def verify_signature(data: bytes, signature_b64: str) -> bool:
    _, public_key = _load_keys()
    signature = base64.b64decode(signature_b64)
    public_key.verify(signature, data)
    return True


def ensure_keys_present() -> bool:
    try:
        _load_keys()
        return True
    except Exception:
        return False

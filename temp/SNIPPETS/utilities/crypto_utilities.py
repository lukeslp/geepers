#!/usr/bin/env python3
"""
Cryptographic Utilities

Description: Lightweight cryptographic helpers for hashing, HMAC signatures,
             key derivation, and optional symmetric encryption using Fernet.

Use Cases:
- API request signing and verification
- Password hashing and key derivation
- Data integrity verification
- Token generation and validation
- Secure configuration encryption
- Session token creation

Dependencies:
- hashlib (standard library)
- hmac (standard library)
- secrets (standard library)
- cryptography (optional, for Fernet encryption)

Notes:
- Fernet encryption requires 'cryptography' package
- PBKDF2 used for secure key derivation from passwords
- HMAC verification uses constant-time comparison
- All functions are pure Python with minimal dependencies

Related Snippets:
- utilities/retry_decorator.py
- utilities/env_config_utilities.py

Source Attribution:
- Extracted from: /home/coolhand/shared/utils/crypto.py
- Author: Luke Steuber
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Optional, Tuple

# Optional Fernet encryption support
try:
    from cryptography.fernet import Fernet
    FERNET_AVAILABLE = True
except ImportError:
    FERNET_AVAILABLE = False

__all__ = [
    "hash_text",
    "generate_hmac",
    "verify_hmac",
    "generate_random_key",
    "derive_key",
    "generate_symmetric_key",
    "encrypt_text",
    "decrypt_text",
    "FERNET_AVAILABLE",
]


def hash_text(text: str, algorithm: str = "sha256") -> str:
    """
    Hash text using the specified algorithm.

    Args:
        text: Text to hash
        algorithm: Hash algorithm (sha256, sha512, md5, sha1, etc.)

    Returns:
        Hexadecimal hash string

    Raises:
        ValueError: If algorithm is not supported
    """
    try:
        hasher = hashlib.new(algorithm)
    except ValueError as exc:
        raise ValueError(f"Unsupported hash algorithm '{algorithm}'") from exc
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


def generate_hmac(message: str, secret: str, algorithm: str = "sha256") -> str:
    """
    Generate a hex-encoded HMAC signature for message.

    Args:
        message: Message to sign
        secret: Secret key for signing
        algorithm: Hash algorithm (default: sha256)

    Returns:
        Hexadecimal HMAC signature
    """
    digest = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        algorithm
    )
    return digest.hexdigest()


def verify_hmac(
    message: str,
    secret: str,
    signature: str,
    algorithm: str = "sha256"
) -> bool:
    """
    Verify an HMAC signature using constant-time comparison.

    Args:
        message: Original message
        secret: Secret key used for signing
        signature: Signature to verify
        algorithm: Hash algorithm used

    Returns:
        True if signature is valid, False otherwise
    """
    expected = generate_hmac(message, secret, algorithm)
    return hmac.compare_digest(expected, signature)


def generate_random_key(length: int = 32) -> str:
    """
    Generate a random hexadecimal key of desired length.

    Args:
        length: Desired key length in hex characters

    Returns:
        Random hexadecimal string

    Raises:
        ValueError: If length is not positive
    """
    if length <= 0:
        raise ValueError("length must be positive")
    # token_hex returns 2 hex chars per byte
    return secrets.token_hex(length // 2 if length % 2 == 0 else (length + 1) // 2)[:length]


def generate_url_safe_token(length: int = 32) -> str:
    """
    Generate a URL-safe random token.

    Args:
        length: Desired token length

    Returns:
        URL-safe base64-encoded token
    """
    return secrets.token_urlsafe(length)


def derive_key(
    password: str,
    *,
    salt: Optional[str] = None,
    iterations: int = 100_000,
    length: int = 32,
    algorithm: str = "sha256",
) -> Tuple[str, str]:
    """
    Derive a key from a password using PBKDF2-HMAC.

    Args:
        password: Password to derive key from
        salt: Optional salt in hex format (auto-generated if None)
        iterations: Number of iterations (default: 100,000)
        length: Desired key length in bytes (default: 32)
        algorithm: Hash algorithm (default: sha256)

    Returns:
        Tuple of (derived_key_hex, salt_hex)
    """
    salt_bytes = bytes.fromhex(salt) if salt else secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        algorithm,
        password.encode("utf-8"),
        salt_bytes,
        iterations,
        dklen=length,
    )
    return derived.hex(), salt_bytes.hex()


def verify_password(
    password: str,
    derived_key: str,
    salt: str,
    iterations: int = 100_000,
    algorithm: str = "sha256"
) -> bool:
    """
    Verify a password against a derived key.

    Args:
        password: Password to verify
        derived_key: Previously derived key in hex
        salt: Salt used during derivation in hex
        iterations: Number of iterations used
        algorithm: Hash algorithm used

    Returns:
        True if password matches, False otherwise
    """
    new_key, _ = derive_key(
        password,
        salt=salt,
        iterations=iterations,
        algorithm=algorithm
    )
    return hmac.compare_digest(new_key, derived_key)


def generate_symmetric_key() -> str:
    """
    Generate a Fernet symmetric encryption key.

    Requires the cryptography package to be installed.

    Returns:
        Fernet key as string

    Raises:
        RuntimeError: If cryptography package is not installed
    """
    if not FERNET_AVAILABLE:
        raise RuntimeError(
            "cryptography package not installed; "
            "install with: pip install cryptography"
        )
    return Fernet.generate_key().decode("utf-8")


def encrypt_text(text: str, key: str) -> str:
    """
    Encrypt text using Fernet symmetric encryption.

    Args:
        text: Text to encrypt
        key: Fernet key (from generate_symmetric_key)

    Returns:
        Encrypted token as string

    Raises:
        RuntimeError: If cryptography package is not installed
    """
    if not FERNET_AVAILABLE:
        raise RuntimeError(
            "cryptography package not installed; "
            "install with: pip install cryptography"
        )
    fernet = Fernet(key.encode("utf-8"))
    token = fernet.encrypt(text.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_text(token: str, key: str) -> str:
    """
    Decrypt text using Fernet symmetric encryption.

    Args:
        token: Encrypted token from encrypt_text
        key: Fernet key used for encryption

    Returns:
        Decrypted plaintext

    Raises:
        RuntimeError: If cryptography package is not installed
        InvalidToken: If token is invalid or key is wrong
    """
    if not FERNET_AVAILABLE:
        raise RuntimeError(
            "cryptography package not installed; "
            "install with: pip install cryptography"
        )
    fernet = Fernet(key.encode("utf-8"))
    plaintext = fernet.decrypt(token.encode("utf-8"))
    return plaintext.decode("utf-8")


def hash_file(filepath: str, algorithm: str = "sha256", chunk_size: int = 8192) -> str:
    """
    Calculate hash of a file.

    Args:
        filepath: Path to file
        algorithm: Hash algorithm (default: sha256)
        chunk_size: Read chunk size in bytes

    Returns:
        Hexadecimal hash string
    """
    hasher = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


# Usage example
if __name__ == "__main__":
    print("Crypto Utilities Demo")
    print("=" * 50)

    # Hashing
    print("\n1. Text Hashing")
    text = "Hello, World!"
    sha256_hash = hash_text(text, "sha256")
    print(f"   Text: {text}")
    print(f"   SHA256: {sha256_hash}")

    sha512_hash = hash_text(text, "sha512")
    print(f"   SHA512: {sha512_hash[:32]}...")

    # HMAC
    print("\n2. HMAC Signatures")
    message = "Important message"
    secret = "my_secret_key"
    signature = generate_hmac(message, secret)
    print(f"   Message: {message}")
    print(f"   HMAC: {signature}")

    # Verify
    is_valid = verify_hmac(message, secret, signature)
    print(f"   Valid: {is_valid}")

    # Tampered
    is_tampered_valid = verify_hmac("tampered", secret, signature)
    print(f"   Tampered Valid: {is_tampered_valid}")

    # Random keys
    print("\n3. Random Key Generation")
    random_key = generate_random_key(32)
    print(f"   Random Key (32): {random_key}")

    url_token = generate_url_safe_token(24)
    print(f"   URL-Safe Token: {url_token}")

    # Key derivation
    print("\n4. Password Key Derivation (PBKDF2)")
    password = "my_secure_password"
    derived_key, salt = derive_key(password, iterations=100_000)
    print(f"   Password: {password}")
    print(f"   Salt: {salt}")
    print(f"   Derived Key: {derived_key[:32]}...")

    # Verify password
    is_correct = verify_password(password, derived_key, salt)
    print(f"   Password Correct: {is_correct}")

    wrong_pass = verify_password("wrong_password", derived_key, salt)
    print(f"   Wrong Password: {wrong_pass}")

    # Fernet encryption (if available)
    print("\n5. Fernet Encryption")
    if FERNET_AVAILABLE:
        key = generate_symmetric_key()
        print(f"   Key: {key[:20]}...")

        secret_text = "This is sensitive data"
        encrypted = encrypt_text(secret_text, key)
        print(f"   Original: {secret_text}")
        print(f"   Encrypted: {encrypted[:40]}...")

        decrypted = decrypt_text(encrypted, key)
        print(f"   Decrypted: {decrypted}")
    else:
        print("   Fernet not available (install cryptography)")

    print("\n" + "=" * 50)
    print("Demo complete!")

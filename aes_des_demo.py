"""
AES & DES Encrypt / Decrypt Demo
================================

Encrypts and decrypts a message with AES (128-bit and 256-bit) and DES,
using the Python `cryptography` library in CBC mode with PKCS7 padding.

Usage:
    python aes_des_demo.py                      # uses the default message
    python aes_des_demo.py "your message here"  # encrypt your own text
"""

import os
import sys
import warnings

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.utils import CryptographyDeprecationWarning

DEFAULT_MESSAGE = "Attack at dawn"


# ---------- helpers ----------

def pad(data: bytes, block_size_bits: int) -> bytes:
    """PKCS7-pad data so its length is a multiple of the cipher's block size."""
    padder = padding.PKCS7(block_size_bits).padder()
    return padder.update(data) + padder.finalize()


def unpad(data: bytes, block_size_bits: int) -> bytes:
    """Remove PKCS7 padding."""
    unpadder = padding.PKCS7(block_size_bits).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def encrypt(algorithm, plaintext: bytes) -> tuple[bytes, bytes]:
    """Encrypt with CBC mode. Returns (iv, ciphertext).

    A fresh random IV is generated for every encryption — never reuse an IV
    with the same key.
    """
    block_bits = algorithm.block_size
    iv = os.urandom(block_bits // 8)
    encryptor = Cipher(algorithm, modes.CBC(iv)).encryptor()
    ciphertext = encryptor.update(pad(plaintext, block_bits)) + encryptor.finalize()
    return iv, ciphertext


def decrypt(algorithm, iv: bytes, ciphertext: bytes) -> bytes:
    """Decrypt CBC-mode ciphertext and strip the padding."""
    decryptor = Cipher(algorithm, modes.CBC(iv)).decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad(padded, algorithm.block_size)


def run_demo(name: str, algorithm, key: bytes, plaintext: bytes) -> None:
    """Encrypt, decrypt and print the results for one cipher."""
    iv, ciphertext = encrypt(algorithm, plaintext)
    recovered = decrypt(algorithm, iv, ciphertext)

    print(f"--- {name} ---")
    print(f"Key        : {key.hex()}  ({len(key) * 8}-bit)")
    print(f"IV         : {iv.hex()}")
    print(f"Ciphertext : {ciphertext.hex()}")
    print(f"Decrypted  : {recovered.decode()}")
    print(f"Match      : {recovered == plaintext}\n")


# ---------- main ----------

def main() -> None:
    message = " ".join(sys.argv[1:]) or DEFAULT_MESSAGE
    plaintext = message.encode("utf-8")
    print(f"Plaintext  : {message}  ({len(plaintext)} bytes)\n")

    # AES: 128-bit block cipher, key can be 128, 192 or 256 bits
    aes128_key = os.urandom(16)
    aes256_key = os.urandom(32)
    run_demo("AES-128-CBC", algorithms.AES(aes128_key), aes128_key, plaintext)
    run_demo("AES-256-CBC", algorithms.AES(aes256_key), aes256_key, plaintext)

    # DES: 64-bit block, 56-bit effective key (8 bytes incl. parity bits).
    # Modern `cryptography` has no standalone DES class, so we use TripleDES
    # with a single 8-byte key — that makes K1 = K2 = K3, which is exactly
    # equivalent to single DES. Included for comparison only: DES is broken
    # and should never be used for real data.
    des_key = os.urandom(8)
    with warnings.catch_warnings():
        # The library warns that DES/3DES is deprecated — we already know.
        warnings.simplefilter("ignore", CryptographyDeprecationWarning)
        des = TripleDES(des_key)
    run_demo("DES-CBC (via TripleDES, single key)", des, des_key, plaintext)


if __name__ == "__main__":
    main()

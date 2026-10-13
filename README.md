# AES-DES-Encrypt-Decrypt

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A short Python demo that encrypts and decrypts a message with **AES-128**, **AES-256**, and **DES**, using the [`cryptography`](https://cryptography.io/) library. Built as part of my cybersecurity coursework at LaGuardia Community College to compare a modern cipher with a legacy one.

## What it does

- Generates random keys with `os.urandom()`
- Encrypts the message in **CBC mode** with a fresh random IV each time
- Applies **PKCS7 padding**, so messages of any length work
- Decrypts and confirms the result matches the original

## Quick start

```bash
git clone https://github.com/kclaughan/AES-DES-Encrypt-Decrypt.git
cd AES-DES-Encrypt-Decrypt
pip install -r requirements.txt

python aes_des_demo.py                       # default message
python aes_des_demo.py "Meet me at midnight" # your own message
```

## Example output

Keys and IVs are random, so your hex values will differ on every run.

```
Plaintext  : Attack at dawn  (14 bytes)

--- AES-128-CBC ---
Key        : 83606d0890084489376ca7c5c62af5bd  (128-bit)
IV         : 9c8f0c6c673eda209b787f8e83a298ac
Ciphertext : 9205ce90f24145e9ec01821578cdb7f0
Decrypted  : Attack at dawn
Match      : True

--- AES-256-CBC ---
Key        : c9c96c20f5a198e99327cdfe667f3c5e5b5b69fde425aba848d9393be8f39a36  (256-bit)
IV         : 7a7e2d4a57bede9918e87470579b3e95
Ciphertext : 9f0b6d0b805392b5a0a6dd124f833bce
Decrypted  : Attack at dawn
Match      : True

--- DES-CBC (via TripleDES, single key) ---
Key        : 6e35aa73e6c2c895  (64-bit)
IV         : 62002b4b74bebe62
Ciphertext : 142e20652dfd5f8da5d28fba36be52af
Decrypted  : Attack at dawn
Match      : True
```

## AES vs DES at a glance

| | AES | DES |
|---|---|---|
| Standardized | 2001 (NIST) | 1977 (NIST) |
| Block size | 128 bits | 64 bits |
| Key size | 128 / 192 / 256 bits | 56 bits effective (64 incl. parity) |
| Status | Current standard | Broken; withdrawn by NIST in 2005 |

DES's 56-bit key can be brute-forced in hours on modern hardware, and its small 64-bit block makes it vulnerable to collision attacks on large amounts of data. AES is the current standard.

## Notes on the implementation

- **Why "DES via TripleDES"?** Recent versions of `cryptography` dropped the standalone DES class. Passing a single 8-byte key to `TripleDES` sets K1 = K2 = K3, which is mathematically equivalent to single DES.
- **Why CBC + padding?** CBC requires input that's an exact multiple of the block size (16 bytes for AES, 8 for DES). PKCS7 padding fills the gap and is removed after decryption.
- **What's missing for real-world use?** CBC provides confidentiality but not integrity, so an attacker could tamper with the ciphertext undetected. In production you'd use an authenticated mode like **AES-GCM** and store keys properly instead of generating them in memory.

> ⚠️ Educational use only. Don't use DES, or this script as-is, to protect real data.

## License

[MIT](LICENSE)

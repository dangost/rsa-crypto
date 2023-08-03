import json
import zlib
import base64
from uuid import uuid4

from tools import password

import jwt
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def save(public_key: bytes, private_key: bytes, path: str = "") -> None:
    name = str(uuid4()).replace('-', '')[0:5]
    with open(f"{path}{name}-public.key", 'wb') as fs:
        fs.write(public_key)

    with open(f"{path}{name}-private.key", 'wb') as fs:
        fs.write(private_key)


def encrypt(data: str, public_key: bytes) -> str:
    key = RSA.import_key(public_key)

    crypter = PKCS1_OAEP.new(key)
    encrypted_key = crypter.encrypt(data.encode("UTF-8"))
    return base64.b64encode(encrypted_key).decode("UTF-8")


def decrypt(encrypted_data: bytes, private_key: bytes, passphrase: str) -> bytes:
    pass


def main():
    passphrase = "pa$$w0rd"
    keys = RSA.generate(1024)
    public_key = keys.publickey().exportKey()
    private_key = keys.export_key(passphrase=passphrase)
    save(public_key, private_key, "keys/")

    compressed = zlib.compress(private_key)
    print(f"key: {len(private_key)} \ncompressed: {len(compressed)}")
    decompressed = zlib.decompress(compressed)

    assert decompressed == private_key

    diff = len(private_key) - len(compressed)
    percents = (1 - (len(compressed) / len(private_key))) * 100
    print(f"keys are equal \ndiff: {diff} bytes, {percents:.1f}%")

    random_key = password.generate(64)

    encrypted_key = encrypt(random_key, public_key)

    with open("data/image.jpg", 'rb') as fs:
        data = fs.read()
    payload = {
        "image": base64.b64encode(data).decode("UTF-8"),
        "message": "Secret image"
    }

    encrypted_data = jwt.encode(payload=payload, algorithm="HS256", key=random_key)

    output = {
        "data": encrypted_data,
        "key": encrypted_key
    }

    with open(f"output/output.json", 'w') as fs:
        json.dump(output, fs)

    pass


main()
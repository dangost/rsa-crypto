import zlib
from uuid import uuid4
from Crypto.PublicKey import RSA


def save(public_key: bytes, private_key: bytes, path: str = "") -> None:
    name = str(uuid4()).replace('-', '')[0:5]
    with open(f"{path}{name}-public.key", 'wb') as fs:
        fs.write(public_key)

    with open(f"{path}{name}-private.key", 'wb') as fs:
        fs.write(private_key)


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


main()
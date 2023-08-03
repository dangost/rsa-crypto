from uuid import uuid4

from bitcoinlib.wallets import Wallet as BitcoinWallet

from wallets.models.walllet import Wallet


def create_wallet() -> Wallet:
    __wallet = BitcoinWallet.create(str(uuid4()))
    private_key: bytes = __wallet.get_key().key_private
    address = __wallet.get_key().address
    return Wallet(address, private_key, "bitcoin")


def init_wallet(private_key: bytes) -> Wallet:
    __wallet = BitcoinWallet.import_key(private_key)


if __name__ == "__main__":
    wallet = create_wallet()
    print(wallet)

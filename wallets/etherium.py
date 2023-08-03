import secrets

from eth_account import Account
from eth_account.signers.local import LocalAccount

from wallets.models.walllet import Wallet


def create_wallet() -> Wallet:
    private_token = secrets.token_hex(32)
    private_key = "0x" + private_token

    account: LocalAccount = Account.from_key(private_key)

    return Wallet(account.address, private_key, "etherium")


def main():
    wallet = create_wallet()

    print(wallet)


if __name__ == "__main__":
    main()

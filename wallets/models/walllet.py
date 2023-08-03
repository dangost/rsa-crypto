from dataclasses import dataclass


@dataclass(frozen=True)
class Wallet:
    address: str
    private_key: str
    network: str

    def __str__(self):
        return f"Address: {self.address} \nPrivate key: {self.private_key}"
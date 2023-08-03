import jwt
import json


def encrypt(path: str, secret_key: str, save_path: str | None = None) -> dict:
    algorithm = "HS256"
    with open(path, 'r') as fs:
        data = json.load(fs)
    filename = path.split('/')[-1]
    description = "Trust wallet backup file"

    payload = {
        "filename": filename,
        "description": description,
        "wallet_data": data
    }
    encrypted = jwt.encode(payload=payload, algorithm=algorithm, key=secret_key)

    result = {
        "encrypt_type": "JWT",
        "algorithm": algorithm,
        "description": "This file was encrypted by gost with secret password",
        "data": encrypted
    }

    if save_path is not None:
        with open(save_path, 'w') as fs:
            json.dump(result, fs)

    return result

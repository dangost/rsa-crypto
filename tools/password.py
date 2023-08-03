import random


def generate(size: int) -> str:
    __keymap = "1234567890-=[];'./,`~!@#$%^&*()_+{}:>?<qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    password = ""
    for _ in range(size):
        password += random.choice(__keymap)
    return password

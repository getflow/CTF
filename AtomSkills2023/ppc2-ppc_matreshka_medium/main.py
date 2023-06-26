import hashlib
import os
import socket
import threading
from _thread import start_new_thread
from typing import Optional

from models.doll import Doll

GAME_NAME = """

⠀⠀⠀⢀⣤⣴⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣾⠛⠉⠉⠙⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡇⠀⠀⠀⠀⠀⡇⠀⢀⣴⠶⠶⢦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣿⣄⣀⣀⣠⣾⡇⠀⢸⠃⠀⠀⠀⢿⠀⠀⡴⠶⠶⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⡀⢸⣦⣀⣀⣠⣇⠀⠀⠀⠀⠀⡹⠀⢀⡴⠶⡄⠀⠀
⠀⠀⠻⠿⢿⣿⣿⣿⠿⠿⠃⢸⣿⣿⣿⣿⣿⡄⢠⣷⣶⣾⣧⠀⢸⣀⢀⡇⠀⠀
⠀⠐⣷⣶⣤⣤⣤⣤⣶⣶⣿⠀⣉⣉⣉⣉⣩⣄⠈⠿⠿⠿⠟⠂⢸⣿⣿⣧⠀⠀
⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⠇⢸⣿⣿⣿⣿⣿⡏⢠⣶⣶⣶⣶⡇⢠⣄⣀⣤⠀⠀
⠀⠀⠀⠻⠿⠿⠿⠿⠿⠋⠀⠘⠿⠿⠿⠿⠟⠀⠘⠿⠿⠿⠟⠀⠸⠿⠿⠏⠀⠀

"""
MATRESHKA_FLAG = str(os.getenv('MATRESHKA_FLAG', 'flag{SupaDupaFlag}'))
MATRESHKA_COUNT = int(os.getenv('MATRESHKA_COUNT', 2))


def generate_matreshka() -> list[Doll]:
    return [Doll.generate(doll_id=i) for i in range(MATRESHKA_COUNT)]


def threaded(conn):
    dolls = generate_matreshka()

    try:
        conn.send(bytes(f"{GAME_NAME}\n", encoding='utf-8'))
        parts = list()

        for doll in dolls:
            while True:
                conn.send(bytes(f"{doll.qr()}\n", encoding='utf-8'))
                data = conn.recv(4096)
                if not data:
                    raise Exception

                user_input = data.decode('utf-8').strip()
                if user_input == doll.key:
                    parts.append(user_input)
                    break
                conn.send(bytes(f"{doll.failed()}\n", encoding='utf-8'))
                raise Exception
        conn.send(bytes(f"You found all the dolls. Give me md5 of all keys you entered (concatenate keys and then md5) to get a flag!\n", encoding='utf-8'))
        key = hashlib.md5("".join(parts).encode("utf-8")).hexdigest()
        print(key)
        data = conn.recv(4096)
        if not data:
            raise Exception

        user_input = data.decode('utf-8').strip()
        if user_input != key:
            raise Exception
        conn.send(bytes(f"{MATRESHKA_FLAG}\n", encoding='utf-8'))
    except:
        print("failed")
    finally:
        conn.close()


if __name__ == '__main__':
    host = ""
    port = 5002

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((host, port))

    generate_matreshka()

    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        print_lock = threading.Lock()
        print("Connected to : ", addr[0], ":", addr[1])

        start_new_thread(threaded, (conn,))

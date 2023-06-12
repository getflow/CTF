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

MATRESHKA: Optional[list[Doll]] = None


def generate_matreshka() -> list[Doll]:
    global MATRESHKA

    if MATRESHKA is None:
        MATRESHKA = [Doll.generate() for _ in range(MATRESHKA_COUNT)]

    return MATRESHKA


def threaded(conn):
    dolls = generate_matreshka()

    try:
        conn.send(bytes(f"{GAME_NAME}\n", encoding='utf-8'))

        for doll in dolls:
            while True:
                conn.send(bytes(f"{doll.qr()}\n", encoding='utf-8'))
                data = conn.recv(4096)
                if not data:
                    raise Exception

                if data.decode('utf-8').strip() == doll.key:
                    break
                conn.send(bytes(f"{doll.failed()}\n", encoding='utf-8'))
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

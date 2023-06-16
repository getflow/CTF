import hashlib
import os
import socket
import threading
from _thread import start_new_thread
from typing import Optional

from models.barcode import Barcode

GAME_NAME = """

         . .
       .. . *.
- -_ _-__-0oOo
 _-_ -__ -||||)
    ______||||______
~~~~~~~~~~`""'⠀

"""
BARCODE_FLAG = str(os.getenv('BARCODE_FLAG', 'flag{SupaDupaFlag}'))
BARCODE_COUNT = int(os.getenv('BARCODE_COUNT', 2))


def generate_barcodes() -> list[Barcode]:
    return [Barcode.generate(barcode_id=i) for i in range(BARCODE_COUNT)]


def threaded(conn):
    barcodes = generate_barcodes()

    try:
        conn.send(bytes(f"{GAME_NAME}\n", encoding='utf-8'))

        for barcode in barcodes:
            while True:
                conn.send(bytes(f"{barcode.qr()}\n", encoding='utf-8'))
                data = conn.recv(4096)
                if not data:
                    raise Exception

                user_input = data.decode('utf-8').strip()
                if user_input == barcode.key:
                    break
                conn.send(bytes(f"{barcode.failed()}\n", encoding='utf-8'))
                raise Exception
        conn.send(bytes(f"{BARCODE_FLAG}\n", encoding='utf-8'))
    except:
        print("failed")
    finally:
        conn.close()


if __name__ == '__main__':
    host = ""
    port = 5002

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((host, port))

    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        print_lock = threading.Lock()
        print("Connected to : ", addr[0], ":", addr[1])

        start_new_thread(threaded, (conn,))

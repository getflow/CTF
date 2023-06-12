import uuid

import atomics
import qrcode
from qrcode.image.svg import SvgPathImage


class Doll:
    __next_door_id: atomics.INT = atomics.atomic(4, atomics.UINT)

    def __init__(self, doll_id: int):
        self.__doll_id = doll_id
        self.__key = f"NOT_FLAG<{uuid.uuid4()}>"

    @staticmethod
    def generate():
        return Doll(doll_id=Doll.next_doll_id())

    def name(self):
        return f"Doll #{self.__doll_id}"

    @staticmethod
    def next_doll_id() -> int:
        return Doll.__next_door_id.fetch_inc()

    @property
    def key(self) -> str:
        old_key = self.__key
        self.__key = f"NOT_FLAG<{uuid.uuid4()}>"
        return old_key

    def qr(self) -> str:
        print(self.__key)
        img = qrcode.make(data=self.__key, image_factory=SvgPathImage)
        return f"""{self.name()}

⠀⠀⠀⢀⣤⣴⣶⣤⣀
⠀⠀⠀⣾⠛⠉⠉⠙⢿⡆
⠀⠀⠀⡇⠀⠀⠀⠀⠀⡇
⠀⠀⠀⣿⣄⣀⣀⣠⣾⡇⠀
⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⡀
⠀⠀⠻⠿⢿⣿⣿⣿⠿⠿⠃
⠀⠐⣷⣶⣤⣤⣤⣤⣶⣶⣿
⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⠇
⠀⠀⠀⠻⠿⠿⠿⠿⠿⠋

{img.to_string(encoding="unicode")}"""

    def failed(self):
        return f"Doll #{self.__doll_id} failed. Try again!"

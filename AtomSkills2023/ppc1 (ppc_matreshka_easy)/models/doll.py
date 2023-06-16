import uuid

import qrcode
from qrcode.image.svg import SvgPathImage


class Doll:
    def __init__(self, doll_id: int):
        self.__doll_id = doll_id
        self.__key = f"NOT_FLAG<{uuid.uuid4()}>"

    @staticmethod
    def generate(doll_id: int):
        return Doll(doll_id=doll_id)

    def name(self):
        return f"Doll #{self.__doll_id}"

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

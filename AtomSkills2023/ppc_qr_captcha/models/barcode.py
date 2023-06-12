import base64
import uuid
from io import BytesIO

import qrcode
from qrcode.image.pure import PyPNGImage


class Barcode:
    def __init__(self, barcode_id: int):
        self.__barcode_id = barcode_id
        self.__key = f"NOT_FLAG<{uuid.uuid4()}>"

    @staticmethod
    def generate(barcode_id: int):
        return Barcode(barcode_id=barcode_id)

    def name(self):
        return f"Glass #{self.__barcode_id}"

    @property
    def key(self) -> str:
        old_key = self.__key
        self.__key = f"NOT_FLAG<{uuid.uuid4()}>"
        return old_key

    def qr(self) -> str:
        print(self.__key)
        img = qrcode.make(data=self.__key, image_factory=PyPNGImage)

        bytes_stream = BytesIO()
        img.save(stream=bytes_stream, kind="png")

        bytes_stream.seek(0)
        encoded = base64.b64encode(bytes_stream.read())
        b64string = encoded.decode("utf-8")

        return f"""{self.name()}

.~~~~.
i====i_
|cccc|_)
|cccc|   hjw
`-==-'

    {b64string}"""

    def failed(self):
        return f"Glass #{self.__barcode_id} failed. Try again!"

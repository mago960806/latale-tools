from dataclasses import dataclass
from typing import BinaryIO, Optional


from latale_extractor.utils import read_float32, read_int32, read_string

IMAGE_DATA_LENGTH = 112


class BadTblFile(Exception):
    pass


@dataclass
class Frame:
    sequence: int
    offset_x: int
    offset_y: int
    center_offset_x: int
    center_offset_y: int
    left: int
    top: int
    right: int
    buttom: int
    texture_name: str
    texture_data: str


class TblReader(object):
    def __init__(
        self,
        file: str,
        encoding: Optional[str] = "BIG5",
    ):
        self._stream: BinaryIO = open(file, "rb")
        self._encoding = encoding
        self.check_tbl_file()
        # self.load()

    def check_tbl_file(self):
        hex_signature = read_int32(self._stream)
        if hex_signature != 0x64:
            raise BadTblFile("File is not a tbl file")

    def load(self):
        data = {}
        total = read_int32(self._stream)
        for _ in range(total):
            count = read_int32(self._stream)
            name = read_string(self._stream, 12, encoding=self._encoding)
            self._stream.read(120)
            frames = []
            for _ in range(count):
                frames.append(
                    Frame(
                        sequence=read_int32(self._stream),
                        offset_x=read_int32(self._stream),
                        offset_y=read_int32(self._stream),
                        center_offset_x=read_float32(self._stream),
                        center_offset_y=read_float32(self._stream),
                        left=read_int32(self._stream),
                        top=read_int32(self._stream),
                        right=read_int32(self._stream),
                        buttom=read_int32(self._stream),
                        texture_name=read_string(self._stream, 16, encoding=self._encoding),
                        # texture_data=self._stream.read(112)
                        texture_data=self._stream.read(112).hex(" ").upper(),
                    )
                )
                frames.sort(key=lambda x: x.sequence)
            data[name] = frames
        return data

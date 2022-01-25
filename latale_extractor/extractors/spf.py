import io
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Optional

from latale_extractor.utils import read_int32, read_string

DEFAULT_ENCODING = "utf-8"


@dataclass
class File:
    path: Path
    position: int
    size: int

    @property
    def filename(self) -> str:
        return self.path.name


class SpfFile(object):
    def __init__(self, file: str, encoding: str = "EUC-KR"):
        self._stream: BinaryIO = open(file, "rb")
        self.encoding = encoding
        self.files: list[File] = []
        self._load()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    @property
    def filenames(self):
        return [file.filename for file in self.files]

    def extract(self, member, path=None):
        raise NotImplementedError()

    def extractall(self, to: Optional[Path] = None):
        for file in self.files:
            self._stream.seek(file.position, io.SEEK_SET)
            if to:
                filepath = to / file.path
            else:
                file.path.parent.mkdir(parents=True, exist_ok=True)
                filepath = file.path
            with open(filepath, "wb") as f:
                f.write(self._stream.read(file.size))

    def close(self):
        self._stream.close()

    def _load(self):
        # 读取文件末尾的版本号和归档编号
        self._stream.seek(-4, io.SEEK_END)
        self._version = read_int32(self._stream)
        self._stream.seek(-136, io.SEEK_END)
        self._archive_number = read_int32(self._stream)
        print(f"版本号为: {self._version}")
        print(f"归档编号为: {self._archive_number}")
        # 读取文件列表
        self._stream.seek(-140, io.SEEK_END)
        files_length = read_int32(self._stream)
        file_count = int(files_length / 140)
        # 循环读取文件
        self._stream.seek(-1 * (files_length + 4), io.SEEK_CUR)
        for _ in range(file_count):
            path = read_string(self._stream, 128, encoding=self.encoding)
            position = read_int32(self._stream)
            size = read_int32(self._stream)
            self.files.append(File(path=Path(path), position=position, size=size))
            self._stream.seek(4, io.SEEK_CUR)

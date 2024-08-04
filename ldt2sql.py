import time
from dataclasses import dataclass
from enum import unique, IntEnum
from pathlib import Path
from typing import BinaryIO
from struct import calcsize

import pandas as pd
from rich.progress import track
from rich import print
import sys
import io
import struct

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "ldt2sql.log"
ROWID_FILE = BASE_DIR / "ROWID.SPF"

FILE_INFO_FORMAT = "128sIII"


@dataclass
class File:
    path: Path
    position: int
    size: int
    index: int


@unique
class FieldType(IntEnum):
    STRING = 1
    BOOL = 2
    INT = 3
    FLOAT = 4


DATA_TYPE_MAP = {
    FieldType.STRING: "string",
    FieldType.BOOL: "boolean",
    FieldType.INT: "UInt32",
    FieldType.FLOAT: "Float32",
}


def read_int16(stream: BinaryIO) -> int:
    return struct.unpack("<H", stream.read(2))[0]


def read_int(stream: BinaryIO) -> int:
    return struct.unpack("<I", stream.read(4))[0]


def read_float(stream: BinaryIO) -> float:
    return struct.unpack("<f", stream.read(4))[0]


def read_string(stream: BinaryIO, /, length: int, encoding: str = "ascii", failback_encoding: str = "CP949") -> str:
    data = stream.read(length)
    try:
        return struct.unpack(f"{length}s", data)[0].rstrip(b"\x20").rstrip(b"\x00").decode(encoding)
    except UnicodeDecodeError:
        return struct.unpack(f"{length}s", data)[0].rstrip(b"\x20").rstrip(b"\x00").decode(failback_encoding)


if not ROWID_FILE.exists():
    print("[red]没有找到 ROWID.SPF 文件[/red]")
    sys.exit(0)

with ROWID_FILE.open("rb") as stream:
    stream.seek(-4, io.SEEK_END)
    version = read_int(stream)
    stream.seek(-136, io.SEEK_END)
    archive_number = read_int(stream)
    print(f"版本号为: {version}")
    print(f"归档编号为: {archive_number}")
    stream.seek(-140, io.SEEK_END)
    files_length = read_int(stream)
    files_count = int(files_length / 140)
    # 跳转到数据区
    stream.seek(-1 * (files_length + 4), io.SEEK_CUR)
    # 读取文件列表
    files = []
    for _ in range(files_count):
        path, position, size, index = struct.unpack(FILE_INFO_FORMAT, stream.read(calcsize(FILE_INFO_FORMAT)))
        path = BASE_DIR / path.rstrip(b"\x00").decode("ascii")
        files.append(File(path, position, size, index))
    # 将文件写入到磁盘上
    # for file in track(files, description="资源文件解压中..."):
    #     with file.path.open("wb") as f:
    #         stream.seek(file.position)
    #         f.write(stream.read(file.size))
    #     time.sleep(0.005)
# 读取 LDT 文件
for file in track(files, description="数据文件解析中..."):
    rows = []
    print(file.path.name)
    with file.path.open("rb") as stream:
        # 读取行列数量
        _, column_count, row_count = struct.unpack("III", stream.read(12))
        # 读取字段名称
        field_names = ["ID"]
        for _ in range(column_count):
            field_name = read_string(stream, 64).lstrip("_")
            field_names.append(field_name)
        # 读取字段类型
        stream.seek(64 * (128 - column_count), io.SEEK_CUR)
        field_types = [FieldType.INT]
        for _ in range(column_count):
            field_type = read_int(stream)
            field_types.append(FieldType(field_type))
        # 读取数据
        stream.seek(4 * (128 - column_count), io.SEEK_CUR)
        for _ in range(row_count):
            field_values = []
            for field_type in field_types:
                match field_type:
                    case FieldType.INT:
                        field_value = read_int(stream)
                    case FieldType.BOOL:
                        field_value = read_int(stream)
                    case FieldType.STRING:
                        length = read_int16(stream)
                        field_value = read_string(stream, length=length, encoding="Big5-HKSCS")
                    case FieldType.FLOAT:
                        field_value = read_float(stream)
                field_values.append(field_value)
            rows.append(field_values)
    # 转换为 DataFrame 对象
    field_types = [DATA_TYPE_MAP[field_type] for field_type in field_types]
    df = pd.DataFrame(rows, columns=field_names).astype(dict(zip(field_names, field_types)))
    # df.to_csv(f"{file.path.name}.csv", index=False)

import struct
from typing import Any, BinaryIO


def read_byte(stream: BinaryIO) -> bytes:
    return _read_as_unpack(stream, "b", 1)


def read_short(stream: BinaryIO) -> int:
    return _read_as_unpack(stream, "h", 2)


def read_int32(stream: BinaryIO) -> int:
    return _read_as_unpack(stream, "l", 4)


def read_int64(stream: BinaryIO) -> int:
    return _read_as_unpack(stream, "q", 8)


def read_float(stream: BinaryIO) -> float:
    return _read_as_unpack(stream, "f", 4)


def read_string(stream: BinaryIO, length: int, encoding: str) -> str:
    data = stream.read(length).split(b"\x00")[0]
    return data.decode(encoding, errors="replace")


def _read_as_unpack(stream: BinaryIO, fmt, length: int) -> Any:
    return struct.unpack("<" + fmt, stream.read(length))[0]


def write_byte(stream: BinaryIO, value: bytes):
    _write_as_pack(stream, 'b', bytes(value))


def write_short(stream: BinaryIO, value: int):
    _write_as_pack(stream, 'h', int(value))


def write_int32(stream: BinaryIO, value: int):
    _write_as_pack(stream, 'l', int(value))

def write_int64(stream: BinaryIO, value: int):
    _write_as_pack(stream, 'q', int(value))


def write_float(stream: BinaryIO, value: float):
    _write_as_pack(stream, 'f', float(value))


def write_string(stream: BinaryIO, value: str, encoding: str):
    stream.write(value.encode(encoding))


def write_pascal_string(stream: BinaryIO, value: str, encoding: str):
    value_bytes = value.encode(encoding, errors="replace")
    write_short(stream, len(value_bytes))
    stream.write(value_bytes)


def write_string_with_pading(stream: BinaryIO, value: str, length: int, encoding: str, padding_char=b'\x00', append_bytes=b""):
    value_bytes = value.encode(encoding) + append_bytes
    padding_bytes = padding_char * (length - len(value_bytes))
    stream.write(value_bytes + padding_bytes)


def _write_as_pack(stream: BinaryIO, fmt, value):
    stream.write(struct.pack('<' + fmt, value))

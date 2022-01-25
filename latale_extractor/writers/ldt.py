import io
from typing import Optional

from latale_extractor.readers import ColumnType, Column
from latale_extractor.utils import write_int32, write_string_with_pading, write_pascal_string, write_float, write_short

COLUMN_COUNT_POSITION = 4  # 列数位于文件 4 字节处
ROW_COUNT_POSITION = 8  # 行数位于文件 8 字节处
COLUMN_NAME_POSITION = 12  # 列名位于文件 12 字节处
COLUMN_TYPE_POSITION = 8204  # 列类型位于文件 8204 字节处
ROW_DATA_POSITION = 8716  # 行数据位于文件 8716 字节处

COLUMN_COUNT_LENGTH = 4  # 列数长度为 4 字节, 类型为 int32
ROW_COUNT_LENGTH = 4  # 行数长度为 4 字节, 类型为 int32
COLUMN_NAME_LENGTH = 64  # 列名长度为 64 字节, 类型为 string


class LdtWriter(object):
    def __init__(self, columns: list[Column], encoding: Optional[str] = "GBK"):
        self._stream = io.BytesIO()
        self._columns = columns
        self._encoding = encoding

    def write(self, data: list[list]):
        # 写入行、列数
        self._stream.seek(4, io.SEEK_SET)
        write_int32(self._stream, len(self._columns) - 1)
        write_int32(self._stream, len(data))
        # 写入列名称
        self._stream.seek(COLUMN_NAME_POSITION, io.SEEK_SET)
        for column in self._columns:
            if column.name == "ID":
                continue
            write_string_with_pading(self._stream, column.name, COLUMN_NAME_LENGTH, encoding=self._encoding,
                                     padding_char=b"\x20", append_bytes=b"\x00")
        # 写入列类型
        self._stream.seek(COLUMN_TYPE_POSITION, io.SEEK_SET)
        for column in self._columns:
            if column.name == "ID":
                continue
            write_int32(self._stream, column.type.value)
        # 写入列数据
        self._stream.seek(ROW_DATA_POSITION, io.SEEK_SET)
        for row in data:
            for index, column in enumerate(self._columns):
                value = row[index]
                if column.type == ColumnType.INT:
                    write_int32(self._stream, value)
                elif column.type == ColumnType.BOOL:
                    write_int32(self._stream, value)
                elif column.type == ColumnType.STRING:
                    write_pascal_string(self._stream, value, encoding=self._encoding)
                elif column.type == ColumnType.FLOAT:
                    write_float(self._stream, value)
                else:
                    raise ValueError(f"invalid column type: {column.type}")
        # END标识
        write_string_with_pading(self._stream, "END", COLUMN_NAME_LENGTH, encoding=self._encoding,
                                 padding_char=b"\x20")

    def save(self, filepath):
        self._stream.seek(io.SEEK_SET)
        with open(filepath, "wb") as f:
            f.write(self._stream.read())

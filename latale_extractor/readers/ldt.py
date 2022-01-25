import io
from dataclasses import dataclass
from enum import IntEnum, unique
from typing import BinaryIO, Optional


from latale_extractor.utils import read_float, read_int32, read_short, read_string

COLUMN_COUNT_POSITION = 4  # 列数位于文件 4 字节处
ROW_COUNT_POSITION = 8  # 行数位于文件 8 字节处
COLUMN_NAME_POSITION = 12  # 列名位于文件 12 字节处
COLUMN_TYPE_POSITION = 8204  # 列类型位于文件 8204 字节处
ROW_DATA_POSITION = 8716  # 行数据位于文件 8716 字节处

COLUMN_COUNT_LENGTH = 4  # 列数长度为 4 字节, 类型为 int32
ROW_COUNT_LENGTH = 4  # 行数长度为 4 字节, 类型为 int32
COLUMN_NAME_LENGTH = 64  # 列名长度为 64 字节, 类型为 string


@unique
class ColumnType(IntEnum):
    UNSIGNED_INT = 0
    STRING = 1
    BOOL = 2
    INT = 3
    FLOAT = 4


@dataclass
class Column:
    name: str
    type: ColumnType


class LdtReader(object):
    def __init__(
        self,
        file,
        encoding: Optional[str] = "GBK",
        auto_trim_whitespace: bool = True,
    ):
        self._stream: BinaryIO = open(file, "rb")
        self.columns: list = []
        self.rows: list = []
        self._encoding = encoding
        self._auto_trim_whitespace = auto_trim_whitespace
        self._load()

    @property
    def column_names(self):
        return [column.name for column in self.columns]

    def _load(self):
        self._stream.seek(4, io.SEEK_SET)
        column_count = read_int32(self._stream)
        row_count = read_int32(self._stream)

        self._load_columns(column_count)
        self._load_rows(row_count)

    def _load_columns(self, column_count):
        # 获取列的名称
        self._stream.seek(COLUMN_NAME_POSITION, io.SEEK_SET)
        column_names = []
        for _ in range(column_count):
            column_name = read_string(self._stream, COLUMN_NAME_LENGTH, encoding=self._encoding)
            column_names.append(column_name)
        # 获取列的类型
        self._stream.seek(COLUMN_TYPE_POSITION, io.SEEK_SET)
        column_types = []
        for _ in range(column_count):
            column_type = read_int32(self._stream)
            column_types.append(ColumnType(column_type))

        # 插入ID列, 为了美观
        id_column = Column("ID", ColumnType.INT)
        self.columns.append(id_column)

        for column_name, column_type in zip(column_names, column_types):
            column = Column(column_name, column_type)
            self.columns.append(column)

    def _load_rows(self, row_count):
        # 获取行数据
        self._stream.seek(ROW_DATA_POSITION, io.SEEK_SET)
        for _ in range(row_count):
            row = []
            for column in self.columns:
                if column.type in (
                    ColumnType.INT,
                    ColumnType.UNSIGNED_INT,
                    ColumnType.BOOL,
                ):
                    row.append(read_int32(self._stream))
                elif column.type == ColumnType.FLOAT:
                    row.append(read_float(self._stream))
                elif column.type == ColumnType.STRING:
                    length = read_short(self._stream)
                    string = read_string(self._stream, length, encoding=self._encoding)
                    if self._auto_trim_whitespace:
                        string = string.strip()
                    row.append(string)
                else:
                    raise ValueError(f"invalid column type: {column.type}")
            self.rows.append(row)

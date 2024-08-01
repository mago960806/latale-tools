import csv
import sys
import argparse
from enum import Enum
from pathlib import Path


from latale_extractor.readers import LdtReader


class LDTEncoding(Enum):
    GB2312 = "gb2312"
    BIG5 = "big5"
    SHIFT_JIS = "shift_jis"
    EUC_KR = "euc-kr"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LDT 转 CSV 命令行工具, 支持台服、韩服、日服、国服")
    # parser.add_argument("files", type=str, nargs="+", help="一个或多个需要转换的 LDT 文件")
    parser.add_argument(
        "-e",
        "--encoding",
        type=str,
        choices=[enc.value for enc in LDTEncoding],
        default=LDTEncoding.BIG5.value,
        help="指定 LDT 文件的编码, 默认为 Big5",
    )

    args = parser.parse_args()

    try:
        while True:
            file = input("请拖拽 LDT 文件到窗口中并按回车继续: ")
            try:
                file = Path(file)
                save_dir = file.parent
                reader = LdtReader(file, encoding=args.encoding)
                with open(save_dir / f"{file.stem}.csv", "w", encoding="utf-8", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(reader.column_names)
                    writer.writerows(reader.rows)
            except Exception as e:
                print(f"转换失败: {e}")
            else:
                print(f"转换成功, 文件保存在 {save_dir.absolute()}")
    except KeyboardInterrupt:
        sys.exit(0)

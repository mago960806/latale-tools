from pathlib import Path
from latale_extractor.readers import LdtReader
import csv


if __name__ == "__main__":
    try:
        while True:
            file = input("请拖拽 LDT 文件到窗口中并按回车继续: ")
            try:
                file = Path(file)
                save_dir = file.parent
                reader = LdtReader(file, encoding="big5")
                with open(save_dir / f"{file.stem}.csv", "w", encoding="utf-8", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(reader.column_names)
                    writer.writerows(reader.rows)
            except Exception as e:
                print(f"转换失败: {e}")
            else:
                print(f"转换成功, 文件保存在 {save_dir.absolute()}")
    except KeyboardInterrupt:
        exit(0)

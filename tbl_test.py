from pathlib import Path
from latale_extractor.readers import TblReader
import json

from typing import Any
from dataclasses import is_dataclass, asdict


class DataClassJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


if __name__ == "__main__":
    try:
        while True:
            file = input("请拖拽 TBL 文件到窗口中并按回车继续: ")
            try:
                file = Path(file)
                save_dir = file.parent
                reader = TblReader(file)
                data = reader.load()
                with open(save_dir / f"{file.stem}.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4, cls=DataClassJSONEncoder)
            except Exception as e:
                print(f"转换失败: {e}")
            else:
                print(f"转换成功, 文件保存在 {save_dir.absolute()}")
    except KeyboardInterrupt:
        exit(0)

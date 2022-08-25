from pathlib import Path

import pandas as pd


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"

EXPORT_FIELD_NAMES = [
    "ID",
    "_Name",
    "_OptionType",
]
EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "ID",
    "道具名稱",
    "鑲嵌類型ID",
]


def export():
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("ITEM_?.csv")])
    df = df.loc[df["_OptionType"] != 0]
    df = df[EXPORT_FIELD_NAMES]
    df.to_csv(f"ITEM.csv", header=EXPORT_FIELD_NAMES_IN_CHINIESE, index=False, encoding="utf-8")


if __name__ == "__main__":
    export()

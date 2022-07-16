from pathlib import Path

import pandas as pd


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"

LDT_NAME = "GLOBAL_MOB"
EXPORT_FIELD_NAMES = [
    "ID",
    "_Name",
    "_Type",
    "_Name_Visible",
    "_Hp_Visible",
    "_Shadow_Visible",
    "_BossHPCount",
]
EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "ID",
    "怪物名稱",
    "怪物類型(?)",
    "怪物名稱顯示",
    "HP血條顯示",
    "影子顯示",
    "BOSS血條數",
]


def export():
    df: pd.DataFrame = pd.read_csv(CSV_PATH / f"{LDT_NAME}.csv")
    df = df.loc[(df["ID"] != 0) & (df["_Type"] != 0)]
    df = df[EXPORT_FIELD_NAMES]
    df.to_csv(f"{LDT_NAME}.csv", header=EXPORT_FIELD_NAMES_IN_CHINIESE, index=False, encoding="utf-8", na_rep="-")


if __name__ == "__main__":
    export()

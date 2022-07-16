from pathlib import Path

import pandas as pd


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"

LDT_NAME = "MOBLOOT"
EXPORT_FIELD_NAMES = [
    "ID",
    "_Name",
    "_XP",
    "_ElyProbability",
    "_ElyMin",
    "_ElyMax",
]
EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "ID",
    "怪物名稱",
    "經驗值",
    "ELY掉落率(%)",
    "最小ELY",
    "最大ELY",
]


def export():
    df: pd.DataFrame = pd.read_csv(CSV_PATH / f"{LDT_NAME}.csv")
    df = df.loc[df["ID"] > 810000000]
    df["_Name"] = ""
    df["_ElyProbability"] = df["_ElyProbability"] / 1000000
    df = df[EXPORT_FIELD_NAMES]
    df.to_csv(f"{LDT_NAME}.csv", header=EXPORT_FIELD_NAMES_IN_CHINIESE, index=False, encoding="utf-8", na_rep="-")


if __name__ == "__main__":
    export()

from pathlib import Path

import pandas as pd


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"

LDT_NAME = "MOBARRANGE"
EXPORT_FIELD_NAMES = [
    "ID",
    "_MobID",
    "_MobName",
    "_MapID",
    "_MapName",
    "_RectLeft",
    "_RectTop",
    "_RectRight",
    "_RectBottom",
    "_Count",
    "_RespawnTime",
    "_RespawnTime2",
    "_BombDropDefault",
    "_BombMinDrops",
    "_BombRanDrops",
    "_BombDropDefault_Easy",
    "_BombMinDrops_Easy",
    "_BombRanDrops_Easy",
    "_BombDropDefault_Hard",
    "_BombMinDrops_Hard",
    "_BombRanDrops_Hard",
    "_DynamicType",
    "_Difficulty_type",
]
EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "ID",
    "怪物ID",
    "怪物名稱",
    "地圖ID",
    "地圖名稱",
    "左",
    "上",
    "右",
    "下",
    "刷新数量",
    "刷新时间1(每0.1秒)",
    "刷新时间2(每0.1秒)",
    "固定包裹掉落數(普通)",
    "最小包裹掉落數(普通)",
    "隨機包裹掉落數(普通)",
    "固定包裹掉落數(簡單)",
    "最小包裹掉落數(簡單)",
    "隨機包裹掉落數(簡單)",
    "固定包裹掉落數(困难)",
    "最小包裹掉落數(困难)",
    "隨機包裹掉落數(困难)",
    "_DynamicType",
    "_Difficulty_type",
]


def export():
    df: pd.DataFrame = pd.read_csv(CSV_PATH / f"{LDT_NAME}.csv")
    df = df.loc[df["ID"] != 0]
    df[["_StageID", "_MapGroupID", "_MapID"]] = df[["_StageID", "_MapGroupID", "_MapID"]].astype(str)
    df["_MapID"] = df[["_StageID", "_MapGroupID", "_MapID"]].agg("-".join, axis=1)
    df["_MobName"] = ""
    df["_MapName"] = ""
    df = df[EXPORT_FIELD_NAMES]
    df.to_csv(f"{LDT_NAME}.csv", header=EXPORT_FIELD_NAMES_IN_CHINIESE, index=False, encoding="utf-8")


if __name__ == "__main__":
    export()

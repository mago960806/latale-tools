from pathlib import Path

import pandas as pd
import csv


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"

LDT_NAME = "GAMBLE_REWARD"
EXPORT_FIELD_NAMES = [
    "ID",
    "_Gamble_ID",
    "_ITEM_ID",
    "_ITEM_Count",
    "_ITEM_Rare",
    "_ITEM_Point",
    "_Effect",
    "_ITEM_ID_2",
    "_ITEM_Count_2",
    "_ITEM_Rare_2",
    "_ITEM_Point_2",
    "_Effect_2",
    "_ITEM_ID_3",
    "_ITEM_Count_3",
    "_ITEM_Rare_3",
    "_ITEM_Point_3",
    "_Effect_3",
    "_ITEM_ID_4",
    "_ITEM_Count_4",
    "_ITEM_Rare_4",
    "_ITEM_Point_4",
    "_Effect_4",
    "_ITEM_ID_5",
    "_ITEM_Count_5",
    "_ITEM_Rare_5",
    "_ITEM_Point_5",
    "_Effect_5",
]
EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "ID",
    "箱子名稱",
    "獎勵名稱",
    "效果名稱",
]


def load_effect() -> dict[int, str]:
    field_names = [
        "ID",
        "_Name",
    ]
    df = pd.read_csv(CSV_PATH / "EFFECT.csv")
    df = df[field_names]
    data = {}
    for _, row in df.iterrows():
        effect_id, effect_name = row
        data[effect_id] = effect_name
    return data


def load_item() -> dict[int, str]:
    field_names = [
        "ID",
        "_Name",
    ]
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("ITEM_?.csv")])
    df = df[field_names]
    data = {}
    for _, row in df.iterrows():
        item_id, item_name = row
        data[item_id] = item_name
    return data


def export():
    df: pd.DataFrame = pd.read_csv(CSV_PATH / f"{LDT_NAME}.csv")
    df = df[EXPORT_FIELD_NAMES]
    df.rename(
        columns={
            "_ITEM_ID": "_ITEM_ID_1",
            "_ITEM_Count": "_ITEM_Count_1",
            "_ITEM_Rare": "_ITEM_Rare_1",
            "_ITEM_Point": "_ITEM_Point_1",
            "_Effect": "_Effect_1",
        },
        inplace=True,
    )
    # 加載數據
    item = load_item()
    effect = load_effect()
    # 寫入數據
    with open(f"{LDT_NAME}.csv", "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(EXPORT_FIELD_NAMES_IN_CHINIESE)
        for _, row in df.iterrows():
            gamble_id = row["_Gamble_ID"]
            gamble_name = item.get(gamble_id)
            rewards = []
            effects = []
            for index in range(1, 6):
                item_id = row[f"_ITEM_ID_{index}"]
                effect_id = row[f"_Effect_{index}"]
                if item_id != 0:
                    item_name = item.get(item_id)
                    item_count = row[f"_ITEM_Count_{index}"]
                    rewards.append(f"{item_name} X{item_count}")
                # row[f"_ITEM_Rare_{index}"]
                # row[f"_ITEM_Point_{index}"]
                if effect_id != 0:
                    effect_name = effect.get(effect_id)
                    effects.append(effect_name)
            rewards = "\n".join(rewards)
            effects = "\n".join(effects)
            writer.writerow([row["ID"], gamble_name, rewards, effects])


if __name__ == "__main__":
    export()

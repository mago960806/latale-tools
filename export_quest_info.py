from pathlib import Path

import pandas as pd
import csv


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"


LDT_NAME = "QUEST_INFO"

EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "任務ID",
    "任務名稱",
    "任務目標",
    "NPC位置",
    "NPC名稱",
    "EXP獎勵",
    "ELY獎勵",
    "道具獎勵",
]


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


def load_quest() -> dict[int, str]:
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("QUEST_?.csv")])
    field_names = ["ID", "_Name"]
    df = df.loc[df["ID"] != 0]
    df = df[field_names]
    data = {}
    for _, row in df.iterrows():
        quest_id, quest_name = row
        data[quest_id] = quest_name
    return data


def load_quest_reward() -> dict[int, dict[str, int]]:
    field_names = ["ID", "_Reward_EXP", "_Reward_Ely", "reward_items"]
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("QUEST_REWARD_?.csv")])
    df = df.loc[df["ID"] != 0]
    df["reward_items"] = df.apply(get_quest_rewards, axis=1)
    df = df[field_names]
    data = {}
    item = load_item()
    for _, row in df.iterrows():
        quest_reward_id, reward_exp, reward_ely, reward_items = row
        data[quest_reward_id] = {
            "reward_exp": reward_exp,
            "reward_ely": reward_ely,
            "reward_items": "\n".join(
                [f"{item.get(reward_item['item_id'])} X{reward_item['count']}" for reward_item in reward_items]
            ),
        }
    return data


def get_quest_rewards(item: pd.Series):
    return [
        {
            "item_id": item[f"_Reward_ItemID{index}"],
            "count": int(item[f"_Reward_StackCount{index}"]),
        }
        for index in range(1, 6)
        if item[f"_Reward_ItemID{index}"] != 0
    ]


def load_quest_info() -> pd.DataFrame:
    # df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("QUEST_INFO_?.csv")])
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "QUEST_INFO_2.csv")
    field_names = [
        "ID",
        "_Purpose",
        "_Place_Info1",
        "_NPC_Info1",
        "_Quest_Kind",
    ]
    df = df.loc[df["ID"] != 0]
    # df = df.loc[(df["ID"] != 0) & (df["_Quest_Kind"] == "副本")]
    df = df[field_names]
    return df


def export():
    # 加載數據
    quest = load_quest()
    quest_info = load_quest_info()
    quest_reward = load_quest_reward()
    # 寫入數據
    with open(f"{LDT_NAME}.csv", "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(EXPORT_FIELD_NAMES_IN_CHINIESE)
        for _, row in quest_info.iterrows():
            quest_id = row["ID"]
            quest_name = quest.get(quest_id)
            try:
                reward_exp, reward_ely, reward_items = quest_reward.get(quest_id).values()
            except AttributeError:
                continue
            writer.writerow(
                [
                    quest_id,
                    quest_name,
                    row["_Purpose"],
                    row["_Place_Info1"],
                    row["_NPC_Info1"],
                    reward_exp,
                    reward_ely,
                    reward_items,
                ]
            )


if __name__ == "__main__":
    export()

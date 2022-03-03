from os import name
from pathlib import Path
from typing import Optional, Any

import pandas as pd
from math import isnan
from dataclasses import asdict, dataclass, is_dataclass, asdict

import json


class DataClassJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


ROWID_FILE = "ROWID.SPF"

TEMP_DIR = Path()

LDT_PATH = Path(TEMP_DIR) / "DATA/LDT"
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"
LDT_PATH.mkdir(parents=True, exist_ok=True)
CSV_PATH.mkdir(parents=True, exist_ok=True)


@dataclass
class Item:
    id: int
    name: str


def load_item() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Name",
    ]
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("ITEM_?.csv")])
    df = df[field_names]
    return df


def load_quest() -> pd.DataFrame:
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("QUEST_?.csv")])
    field_names = ["ID", "_Quest_BaseLV", "_Quest_Kind"]
    df = df.loc[df["ID"] != 0]
    df = df[field_names]
    return df


def load_quest_info() -> pd.DataFrame:
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("QUEST_INFO_?.csv")])
    field_names = [
        "ID",
        "_Place_Info1",
        "_NPC_Info1",
        "_Place_Info2",
        "_NPC_Info2",
        "_Quest_BaseLV",
        "_Quest_Kind",
        "_Quest_Npcposition",
        "_Quest_Purpseposition",
    ]
    df = df.loc[df["ID"] != 0]
    df = df[field_names]
    return df


def load_quest_reward() -> list[dict]:
    field_names = ["ID", "_Reward_EXP", "_Reward_Ely", "reward_items"]
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("QUEST_REWARD_?.csv")])
    df = df.loc[df["ID"] != 0]
    df["reward_items"] = df.apply(get_quest_rewards, axis=1)
    df = df[field_names]
    item_df = load_item()
    quest_df = load_quest()

    quest_rewards = []
    for _, row in df.iterrows():
        quest_reward_id, reward_exp, reward_ely, reward_items = row
        quest_name = get_quest_name_by_id(quest_reward_id, quest_df)
        if str(reward_exp) == "nan":
            reward_exp = 0
        rewards = []
        for reward_item in reward_items:
            item = get_item_by_id(reward_item["item_id"], item_df)
            rewards.append(f"{item.name} X{reward_item['count']}")
        quest_rewards.append(
            {
                "id": quest_reward_id,
                "name": quest_name,
                "reward_exp": int(reward_exp),
                "reward_ely": int(reward_ely),
                "reward_items": rewards,
            }
        )
    return quest_rewards


def get_quest_rewards(item: pd.Series):
    return [
        {
            "item_id": item[f"_Reward_ItemID{index}"],
            "count": int(item[f"_Reward_StackCount{index}"]),
        }
        for index in range(1, 6)
        if item[f"_Reward_ItemID{index}"] != 0
    ]


def get_item_by_id(item_id: int, item_df: pd.DataFrame) -> Optional[Item]:
    row = item_df[item_df["ID"] == item_id]
    if not row.empty:
        return Item(id=item_id, name=row.iloc[0]["_Name"])


def get_quest_name_by_id(quest_id: int, quest_df: pd.DataFrame) -> str:
    row = quest_df[quest_df["ID"] == quest_id]
    if not row.empty:
        return row.iloc[0]["_Name"]


if __name__ == "__main__":
    item = load_item()
    quest_rewards = load_quest_reward()
    quest_info = load_quest_info()
    with open("quest_rewards.json", "w", encoding="utf-8") as f:
        json.dump(quest_rewards, f, cls=DataClassJSONEncoder, ensure_ascii=False)
    import csv

    with open("quest_rewards.csv", "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=quest_rewards[0].keys())
        writer.writeheader()
        for quest_reward in quest_rewards:
            quest_reward["reward_items"] = "\n".join(quest_reward["reward_items"])
        writer.writerows(quest_rewards)

    quest_info.to_csv("quest_info.csv")

    # mob_loot_with_name = pd.merge(mob_loot, mob, left_on="ID", right_on="ID")
    # print(mob_loot_with_name.to_csv("mob_loot.csv"))

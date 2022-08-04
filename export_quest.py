from pathlib import Path

import pandas as pd
import csv


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"


LDT_NAME = "STORY_QUEST"

EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "任務ID",
    "任務名稱",
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


def load_story_quest() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "STORY_QUEST.csv")
    df = df.loc[df["_Quest_Link"] != 0]
    df = df[["_Name", "_Quest_Link"]]
    return df


def load_story_quest_list() -> dict[int, list[int]]:
    field_names = [
        "ID",
        "_QuestID1",
        "_QuestID2",
        "_QuestID3",
        "_QuestID4",
        "_QuestID5",
        "_QuestID6",
        "_QuestID7",
        "_QuestID8",
        "_QuestID9",
        "_QuestID10",
        "_QuestID11",
        "_QuestID12",
        "_QuestID13",
        "_QuestID14",
        "_QuestID15",
        "_QuestID16",
        "_QuestID17",
        "_QuestID18",
        "_QuestID19",
        "_QuestID20",
        "_QuestID21",
        "_QuestID22",
        "_QuestID23",
        "_QuestID24",
        "_QuestID25",
        "_QuestID26",
        "_QuestID27",
        "_QuestID28",
        "_QuestID29",
        "_QuestID30",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "STORY_QUESTLIST.csv")
    df = df[field_names]
    data = {}
    for _, row in df.iterrows():
        story_quest_id, *quest_ids = row
        data[story_quest_id] = [quest_id for quest_id in quest_ids if quest_id != 0]
    return data


def export():
    # 加載數據
    story_quest = load_story_quest()
    quest = load_quest()
    story_quest_list = load_story_quest_list()
    quest_reward = load_quest_reward()
    # 寫入數據
    with open(f"{LDT_NAME}.csv", "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(EXPORT_FIELD_NAMES_IN_CHINIESE)
        for _, row in story_quest.iterrows():
            quest_ids = story_quest_list.get(row["_Quest_Link"])
            for quest_id in quest_ids:
                quest_name = quest.get(quest_id)
                reward_exp, reward_ely, reward_items = quest_reward.get(quest_id).values()
                writer.writerow([quest_id, quest_name, reward_exp, reward_ely, reward_items])


if __name__ == "__main__":
    export()

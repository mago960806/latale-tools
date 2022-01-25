from pathlib import Path

import pandas as pd

ROWID_FILE = "ROWID.SPF"

TEMP_DIR = Path()

LDT_PATH = Path(TEMP_DIR) / "DATA/LDT"
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"
LDT_PATH.mkdir(parents=True, exist_ok=True)
CSV_PATH.mkdir(parents=True, exist_ok=True)


def get_rewards(item: pd.Series):
    return [
        {
            "id": item[f"_Reward_ID{index}"],
            "probablity": item[f"_Reward_Probablity{index}"],
        }
        for index in range(1, 21)
        if item[f"_Reward_ID{index}"] != 0
    ]


def load_star_tree() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "STAR_TREE.csv")
    df["rewards"] = df.apply(get_rewards, axis=1)
    return df


def load_star_tree_reward() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "STAR_TREE_REWARD.csv")
    return df


def load_item() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Name",
        "_Description",
        "_RGB",
    ]
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("ITEM_?.csv")])
    # RGB
    df["_RGB"] = df[
        [
            "_Red",
            "_Green",
            "_Blue",
        ]
    ].values.tolist()
    df["_RGB"] = df["_RGB"].apply(lambda x: ",".join(map(str, x)))
    df = df[field_names]
    return df



if __name__ == "__main__":
    star_tree = load_star_tree()
    item = load_item()
    item.to_csv("items.csv")
    for index, item in star_tree.iterrows():
        for reward in item["rewards"]:
            print(item["ID"], item["_Growth"], reward["id"], reward["probablity"])

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


@dataclass
class ItemDrop:
    item: Item
    drop_rate: float = 0.0


@dataclass
class ItemSet:
    id: int
    items: list[ItemDrop]


@dataclass
class Loot:
    item: Optional[Item] = None
    itemset: Optional[ItemSet] = None
    drop_rate: float = 0.0


@dataclass
class Mob:
    id: int
    name: str
    xp: int
    ely_min: int
    ely_max: int
    ely_avg: float
    loots: list[Loot]


def chunks(data: list, n: int):
    """Yield successive n-sized chunks from data."""
    for i in range(0, len(data), n):
        yield data[i : i + n]


def load_mob() -> list[Mob]:
    field_names = [
        "ID",
        "_Name",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "GLOBAL_MOB.csv")
    df = df[field_names]
    df = df.loc[df["ID"] != 0]
    mob_loot_df = load_mob_loot()
    item_df = load_item()
    itemsets = load_itemset(item_df)

    mobs = []
    for _, row in df.iterrows():
        mob_id, name = row
        if str(name) == "nan":
            name = None
        mob_loot = get_mob_loot_by_id(mob_id=mob_id, mob_loot_df=mob_loot_df)
        if mob_loot is not None:
            _, xp, _, ely_min, ely_max, *drops = mob_loot
            ely_avg = (ely_min + ely_max) / 2
            loots = []
            for drop in chunks(drops, 4):
                item_id, drop_rate, *_ = drop
                drop_rate = drop_rate / 10000
                if item_id == 0 or drop_rate == 0.0:
                    continue
                item = get_item_by_id(item_id=item_id, item_df=item_df)
                if not item:
                    itemset = get_itemset_by_id(itemset_id=item_id, itemsets=itemsets)
                    if not itemset:
                        continue
                        # raise ValueError(f"怪物掉落了未知物品: {item_id}")
                    else:
                        loots.append(Loot(itemset=itemset, drop_rate=drop_rate))
                else:
                    loots.append(Loot(item=item, drop_rate=drop_rate))
            mob = Mob(id=mob_id, name=name, xp=xp, ely_min=ely_min, ely_max=ely_max, ely_avg=ely_avg, loots=loots)
            mobs.append(mob)
        # else:
        #     print(f"该怪物无信息: {mob_id}")
    return mobs


def load_mob_loot() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "MOBLOOT.csv")
    return df


def load_item() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Name",
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


def get_item_by_id(item_id: int, item_df: pd.DataFrame) -> Optional[Item]:
    row = item_df[item_df["ID"] == item_id]
    if not row.empty:
        return Item(id=item_id, name=row.iloc[0]["_Name"])


def get_mob_loot_by_id(mob_id: int, mob_loot_df: pd.DataFrame) -> Optional[str]:
    row = mob_loot_df[mob_loot_df["ID"] == mob_id]
    if not row.empty:
        return row.iloc[0]


def get_itemset_by_id(itemset_id: int, itemsets: list[ItemSet]) -> Optional[ItemSet]:
    for itemset in itemsets:
        if itemset.id == itemset_id:
            return itemset


def load_itemset(item_df: pd.DataFrame) -> list[ItemSet]:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "ITEMSET.csv")
    itemsets = []
    for _, row in df.iterrows():
        row = iter(row)
        id = next(row)
        items = []
        for item_id, drop_rate in [*zip(row, row)]:
            # 过滤空数据
            if item_id == 0:
                continue
            item = get_item_by_id(item_id, item_df)
            if item:
                items.append(ItemDrop(item=item, drop_rate=drop_rate))
            else:
                raise ValueError(f"存在未知道具ID: {item_id}")
        if items:
            itemsets.append(ItemSet(id=id, items=items))
    return itemsets


if __name__ == "__main__":
    item = load_item()
    mobs = load_mob()
    itemsets = load_itemset(item)
    with open("item_sets.json", "w", encoding="utf-8") as f:
        json.dump(itemsets, f, cls=DataClassJSONEncoder, ensure_ascii=False)
    with open("mobs.json", "w", encoding="utf-8") as f:
        json.dump(mobs, f, cls=DataClassJSONEncoder, ensure_ascii=False)

    # mob_loot_with_name = pd.merge(mob_loot, mob, left_on="ID", right_on="ID")
    # print(mob_loot_with_name.to_csv("mob_loot.csv"))

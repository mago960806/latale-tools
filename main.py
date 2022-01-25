import csv
from pathlib import Path

import pandas as pd
from rich.progress import track

from latale_extractor import SpfFile, LdtReader

ROWID_FILE = "ROWID.SPF"

# TEMP_DIR = Path(tempfile.TemporaryDirectory().name)
TEMP_DIR = Path()

LDT_PATH = Path(TEMP_DIR) / "DATA/LDT"
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"
LDT_PATH.mkdir(parents=True, exist_ok=True)
CSV_PATH.mkdir(parents=True, exist_ok=True)


def init():
    with SpfFile(ROWID_FILE) as spf_file:
        spf_file.extractall(to=TEMP_DIR)
        ldt_files = list(LDT_PATH.glob("*.LDT"))
        for ldt_file in track(ldt_files, description="数据初始化中..."):
            reader = LdtReader(ldt_file, encoding="big5")
            with open(CSV_PATH / f"{ldt_file.stem}.csv", "w", encoding="utf-8", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(reader.column_names)
                writer.writerows(reader.rows)


def load():
    load_items()
    load_mobs()
    load_mob_loots()


def load_items():
    item_df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("ITEM_?.csv")])
    print(f"道具数据加载成功, 共 {len(item_df)} 条数据")
    return item_df

def load_mobs():
    mobs_df = pd.read_csv(CSV_PATH / "GLOBAL_MOB.csv")
    print(f"怪物数据加载成功, 共 {len(mobs_df)} 条数据")
    return mobs_df

def load_mob_loots():
    mob_loots = pd.read_csv(CSV_PATH / "MOBLOOT.csv")
    print(f"包裹数据加载成功, 共 {len(mob_loots)} 条数据")
    return mob_loots

if __name__ == '__main__':
    init()
from pathlib import Path
import csv

import pandas as pd
from itertools import groupby
from operator import itemgetter

TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"


field_names = [
    "ID",
    "_Skill_ID",
    "_Order",
    "_Awaken_Order",
    "_EffectRequire_Value",
]


def load_skill() -> dict[int, str]:
    field_names = [
        "ID",
        "_Name",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL.csv")
    df = df.loc[df["ID"] != 0]
    df = df[field_names]
    data = {}
    for _, row in df.iterrows():
        skill_id, skill_name = row
        data[skill_id] = skill_name
    return data


def load_skill_use():
    df = pd.read_csv(CSV_PATH / "SKILL_USE.csv")
    df = df.loc[df["_Skill_ID"] != 0]
    # df = df.loc[(df["_Skill_ID"] != 0) & (df["_EffectRequire_ID"] == 1)]
    df = df[field_names]
    return df.to_dict("records")


def load_effect():
    df = pd.read_csv(CSV_PATH / "EFFECT.csv")
    df = df.loc[df["ID"] != 0]
    df = df.fillna(0)
    data = {}
    for _, row in df.iterrows():
        data[int(row["ID"])] = int(row["_RequireAction"])
    return data


SKILL = load_skill()
SKILL_USE = load_skill_use()
EFFECT = load_effect()


def check_groups(groups):
    values = set()
    for group in groups:
        values.add(group["_Skill_CoolTimeID"])
    flag = False
    for group in groups:
        if group["_Skill_CoolTimeID"] != group["_CoolTimeApplyID1"]:
            flag = True
    return flag and len(values) > 1


def check_effect(effect_id):
    require_action = EFFECT.get(effect_id)
    return require_action == 0


with open("二段技能.csv", "w", encoding="utf-8", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["ID", "技能ID", "技能阶段", "技能觉醒阶段", "技能释放条件ID", "技能名称"])

    for keys, groups in groupby(SKILL_USE, key=itemgetter("_Skill_ID", "_Awaken_Order")):
        groups = list(groups)
        if len(groups) > 1:
            print("-----------------")
            if any([check_effect(group["_EffectRequire_Value"]) for group in groups]):
                for group in groups:
                    skill_name = SKILL.get(group["_Skill_ID"])
                    print(group)
                    row = [*group.values(), skill_name]
                    writer.writerow(row)
            print("-----------------")

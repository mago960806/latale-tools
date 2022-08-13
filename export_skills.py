from pathlib import Path
import csv

import pandas as pd

ROWID_FILE = "ROWID.SPF"

TEMP_DIR = Path()

LDT_PATH = Path(TEMP_DIR) / "DATA/LDT"
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"
LDT_PATH.mkdir(parents=True, exist_ok=True)
CSV_PATH.mkdir(parents=True, exist_ok=True)


def load_skill() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Name",
        "_MaxSlv",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL.csv")
    df = df.loc[df["ID"] != 0]
    df = df[field_names]
    return df


def load_skill_use() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL_USE.csv")
    df = df.loc[df["_Skill_ID"] != 0]
    return df


def load_effect() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "EFFECT.csv")
    df = df.loc[(df["ID"] != 0) & (df["_StatusEffectType"].isin([10001, 20002, 30001]))]
    return df


def get_effect_by_id(effect_id: int, effect_df: pd.DataFrame):
    row = effect_df[effect_df["ID"] == effect_id]
    if not row.empty:
        return row.iloc[0]


def export():
    skill_df = load_skill()
    skill_use_df = load_skill_use()
    effect_df = load_effect()

    with open("skills.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["技能ID", "技能名称", "技能等级", "技能顺序", "觉醒技能顺序", "基礎技能係數", "每級技能係數", "基礎追加技能傷害", "每級追加技能傷害", "技能倍率"])

        for _, skill in skill_df.iterrows():
            for _, skill_use in skill_use_df[skill_use_df["_Skill_ID"] == skill["ID"]].iterrows():
                effects = set()
                skill_name = skill["_Name"]
                awaken_order = skill_use["_Awaken_Order"]
                # if awaken_order != 0:
                #     skill_name = skill_name
                for index in range(1, 7):
                    effects.add(int(skill_use[f"_Effect_Target{index}"]))
                for index in range(1, 3):
                    effects.add(int(skill_use[f"_Loop_Effect_Target{index}"]))
                if 0 in effects:
                    effects.remove(0)
                effects = list(effects)
                if effects:
                    for index, effect_id in enumerate(effects):
                        effect = get_effect_by_id(effect_id, effect_df)
                        if effect is not None:
                            writer.writerow(
                                [
                                    skill["ID"],
                                    skill_name,
                                    skill["_MaxSlv"],
                                    skill_use["_Order"],
                                    awaken_order,
                                    effect["_EffectParameter1"],
                                    effect["_EffectParameter2"],
                                    effect["_EffectParameter3"],
                                    effect["_EffectParameter4"],
                                    (100 + effect["_EffectParameter1"] + skill["_MaxSlv"] * effect["_EffectParameter2"])
                                    / 100,
                                ]
                            )
                        else:
                            print(skill["ID"], skill["_Name"], "没有战斗效果")
                else:
                    print(skill["ID"], skill["_Name"], "不是攻击类技能")


if __name__ == "__main__":
    export()

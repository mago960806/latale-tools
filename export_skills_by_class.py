import csv
from pathlib import Path


import pandas as pd


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"


def load_classes() -> dict[int:str]:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "CLASS_NAME.csv")
    data = {}
    for _, row in df.iterrows():
        class_id, class_name = row
        data[class_id] = class_name
    return data


def load_skill_main_menu() -> dict[int, list[int]]:
    field_names = ["_Class", "_SubID1", "_SubID2", "_SubID3", "_SubID4", "_SubID5", "_SubID6", "_SubID7", "_SubID8"]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL_MAIN_MENU.csv")
    df = df[field_names]

    data = {}
    for _, row in df.iterrows():
        class_id, *sub_menu_ids = row
        if class_id in data:
            data[class_id].extend(sub_menu_ids)
        else:
            data[class_id] = sub_menu_ids
    for class_id, sub_menu_ids in data.items():
        data[class_id] = [
            sub_menu_id
            for sub_menu_id in sub_menu_ids
            if sub_menu_id
            not in [
                0,
                460,
                461,
                501,
                502,
                504,
                505,
                506,
                507,
                508,
                509,
                510,
                2405,
                2406,
                2407,
                2408,
                2310,
                2409,
                2410,
                2411,
                1316,
                2412,
                2414,
                2434,
                4104,
                4204,
                4107,
                5304,
                6002,
                6402,
                6802,
                7302,
            ]
        ]
    return data


def load_skill_sub_menu() -> dict[int, str]:
    field_names = [
        "ID",
        "_Name",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL_SUB_MENU.csv")
    df = df.loc[(df["ID"] != 0) & df["_Type"] == 1]
    df = df[field_names]
    data = {}
    for _, row in df.iterrows():
        sub_menu_id, sub_menu_name = row
        data[sub_menu_id] = sub_menu_name
    return data


def load_skill_content() -> dict[int, list[int]]:
    field_names = [
        "_SubID",
        "_SkillID",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL_CONTENT.csv")
    df = df.loc[df["_SkillID"] != 0]
    df = df[field_names]
    data = {}
    for _, row in df.iterrows():
        sub_menu_id, skill_id = row
        if sub_menu_id in data:
            data[sub_menu_id].append(skill_id)
        else:
            data[sub_menu_id] = [skill_id]
    return data


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


def load_legend_skill() -> dict[int, list[int]]:
    field_names = [
        "_CLASS",
        "_QuestGroup1_LearnSkill",
        "_QuestGroup2_LearnSkill",
        "_QuestGroup3_LearnSkill",
        "_QuestGroup4_LearnSkill",
        "_QuestGroup5_LearnSkill",
        "_QuestGroup6_LearnSkill",
        "_QuestGroup7_LearnSkill",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "LEGEND_SKILL.csv")
    df = df[field_names]

    data = {}
    for _, row in df.iterrows():
        class_id, *skill_ids = row
        if class_id in data:
            data[class_id].extend(skill_ids)
        else:
            data[class_id] = skill_ids
    return data


def export():
    classes = load_classes()
    skill_main_menu = load_skill_main_menu()
    skill_sub_menu = load_skill_sub_menu()
    skill_content = load_skill_content()
    skill = load_skill()
    legend_skill = load_legend_skill()

    exclude_keywords = ["熟練"]

    with open("skills_by_class.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["职业ID", "职业名称", "技能页ID", "技能页名称", "技能ID", "技能名称"])

        for class_id, class_name in classes.items():
            if class_id in [
                24,
                25,
                26,
                27,
                28,
                29,
                30,
                31,
                32,
                36,
                37,
                38,
                39,
                40,
                41,
                42,
                43,
                44,
                45,
                49,
                52,
                56,
                60,
                64,
                68,
                69,
                73,
                74,
                75,
            ]:
                sub_menu_ids = skill_main_menu.get(class_id)
                for sub_menu_id in sub_menu_ids:
                    sub_menu_name = skill_sub_menu.get(sub_menu_id)
                    if sub_menu_name and sub_menu_name not in [
                        "攻擊輔助技能",
                        "防禦輔助技能",
                        "實用輔助技能",
                        "一般特性",
                        "超越特性",
                    ]:
                        skill_ids = skill_content.get(sub_menu_id)
                        legend_skill_ids = legend_skill.get(class_id)
                        for skill_id in skill_ids:
                            skill_name = skill.get(skill_id)
                            if all([skill_name not in keyword for keyword in exclude_keywords]):
                                writer.writerow(
                                    [class_id, class_name, sub_menu_id, sub_menu_name, skill_id, skill_name]
                                )
                        for legend_skill_id in legend_skill_ids:
                            legend_skill_name = skill.get(legend_skill_id)
                            writer.writerow(
                                [class_id, class_name, sub_menu_id, sub_menu_name, legend_skill_id, legend_skill_name]
                            )


if __name__ == "__main__":
    export()

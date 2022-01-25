import json
from functools import lru_cache
from pathlib import Path


import pandas as pd

ROWID_FILE = "ROWID.SPF"

TEMP_DIR = Path()

LDT_PATH = Path(TEMP_DIR) / "DATA/LDT"
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"
LDT_PATH.mkdir(parents=True, exist_ok=True)
CSV_PATH.mkdir(parents=True, exist_ok=True)


def load_skill() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL.csv")
    df = df.loc[df["ID"] != 0]
    df = df.drop(columns=["_SubID"])
    return df


def load_skill_content() -> pd.DataFrame:
    field_names = [
        "ID",
        "_SubID",
        "_Grid_Index",
        "_SkillID",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL_CONTENT.csv")
    df = df[field_names]
    df = df.loc[df["_SkillID"] != 0]
    return df


def load_skill_main_menu() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Class",
        "_SubID",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL_MAIN_MENU.csv")
    df = df.loc[df["ID"] != 0]
    df["_SubID"] = df[
        [
            "_SubID1",
            "_SubID2",
            "_SubID3",
            "_SubID4",
            "_SubID5",
            "_SubID6",
            "_SubID7",
            "_SubID8",
        ]
    ].values.tolist()
    # 保留非 0 的值
    df["_SubID"] = df["_SubID"].apply(
        lambda items: [item for item in items if item != 0]
    )
    # 去除非戰鬥技能
    df = df[~df["_SubID"].isin([[450, 451, 460], [101], [501, 502], [470]])]
    # 去除格鬥技能
    df["_SubID"] = df["_SubID"].apply(
        lambda items: [item for item in items if item != 510]
    )
    df = df[field_names]
    return df


def load_skill_sub_menu() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Type",
        "_Name",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "SKILL_SUB_MENU.csv")
    df = df.loc[(df["ID"] != 0) & df["_Type"] == 1]
    df = df[field_names]
    return df


def load_classes() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(CSV_PATH / "CLASS_NAME.csv")
    return df


def get_skills_by_sub_id(sub_id: int) -> list[dict]:
    field_names = [
        "ID",
        "_BaseSlv",
        "_MaxSlv",
        "_GetSkillLv",
        "_GetSkillID",
        "_UpRequireSkillPoint",
        "_UpRequireSkillPointSlv",
        "_UpRequire1_Type",
        "_UpRequire1_ID",
        "_UpRequire1_Value1",
        "_UpRequire1_ValueSlv1",
        "_UpRequire1_Value2",
        "_UpRequire1_ValueSlv2",
        "_UpRequire2_Type",
        "_UpRequire2_ID",
        "_UpRequire2_Value1",
        "_UpRequire2_ValueSlv1",
        "_UpRequire2_Value2",
        "_UpRequire2_ValueSlv2",
        "_Icon",
        "_IconIndex",
        "_Learn_Skill",
        "_Name",
        "_Description",
        "_Grid_Index",
        "_Require1_Type",
        "_Require1_ID",
        "_Require1_Value1",
        "_Require1_Value2",
        "_Require2_Type",
        "_Require2_ID",
        "_Require2_Value1",
        "_Require2_Value2",
    ]
    skill_content[
        [
            "_Require1_Type",
            "_Require1_ID",
            "_Require1_Value1",
            "_Require1_Value2",
            "_Require2_Type",
            "_Require2_ID",
            "_Require2_Value1",
            "_Require2_Value2",
        ]
    ] = skill_content[
        [
            "_UpRequire1_Type",
            "_UpRequire1_ID",
            "_UpRequire1_Value1",
            "_UpRequire1_Value2",
            "_UpRequire2_Type",
            "_UpRequire2_ID",
            "_UpRequire2_Value1",
            "_UpRequire2_Value2",
        ]
    ]
    return skill_content[skill_content["_SubID"] == sub_id][field_names].to_dict(
        orient="records"
    )


@lru_cache
def get_sub_name_by_sub_id(sub_id) -> str:
    return skill_sub_menu[skill_sub_menu["ID"] == sub_id].values[0][2]


if __name__ == "__main__":
    skill = load_skill()
    skill_content = load_skill_content()
    skill_main_menu = load_skill_main_menu()
    skill_sub_menu = load_skill_sub_menu()

    skill_content = (
        pd.merge(
            skill_content, skill, suffixes=("_x", ""), left_on="_SkillID", right_on="ID"
        )
        .sort_values("ID_x")
        .drop(columns=["ID_x", "_SkillID"])
    )

    for _, row in skill_main_menu.iterrows():
        data = []
        with open(f"{row['_Class']}.json", "w") as f:
            for sub_id in row["_SubID"]:
                data.append(
                    {
                        "id": sub_id,
                        "name": get_sub_name_by_sub_id(sub_id),
                        "skills": get_skills_by_sub_id(sub_id),
                    }
                )
            json.dump(data, f)

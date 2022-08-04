from pathlib import Path

import pandas as pd
import csv


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"


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


LDT_NAME = "ITEM_UPGRADE"
EXPORT_FIELD_NAMES = [
    "ID",
    "_Main_Item",
    "_Material",
    # "_Probability_Min",
    "_Probability_Max",
    "_Probability_Modifier",
    "_charge",
    "_Result",
    "_Result_massage",
]
EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "ID",
    "裝備名稱",
    "强化材料",
    # "最小成功率",
    "成功率",
    "是否吃镶嵌加成",
    "手續費",
    "强化后裝備名稱",
    "提示信息",
]

ITEM_DB = load_item()


def get_materials(item: pd.Series) -> str:
    materials = []
    for index in range(1, 4):
        if item[f"_Material{index}"] != 0:
            material_id = item[f"_Material{index}"]
            material_name = ITEM_DB.get(material_id)
            count = item[f"_Material_Count{index}"]
            materials.append(f"{material_name} X{count}")
    return "\n".join(materials)


def get_probability_modifier(item: pd.Series) -> str:
    return "否" if item["_Probability_Modifier"] >= 0 else "是"


def export():
    df: pd.DataFrame = pd.read_csv(CSV_PATH / f"{LDT_NAME}.csv")
    df = df.loc[df["_Type"] == 1]
    df["_Main_Item"] = df["_Main_Item"].map(ITEM_DB)
    df["_Result"] = df["_Result"].map(ITEM_DB)
    df["_Probability_Modifier"] = df.apply(get_probability_modifier, axis=1)
    df["_Material"] = df.apply(get_materials, axis=1)
    df = df[EXPORT_FIELD_NAMES]
    df.to_csv(f"{LDT_NAME}.csv", header=EXPORT_FIELD_NAMES_IN_CHINIESE, index=False, encoding="utf-8")


if __name__ == "__main__":
    export()

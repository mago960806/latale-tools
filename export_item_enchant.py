from pathlib import Path

import pandas as pd
import csv


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"
LDT_NAME = "ITEM_ENCHANT"

EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "ID",
    "鑲嵌類型ID",
    "鑲嵌屬性名稱",
    "自然最小數值",
    "自然最大數值",
    "鑲嵌最小數值",
    "鑲嵌最大數值",
    "鑲嵌材料",
    "最小耐久度消耗",
    "最大耐久度消耗",
    "概率補正",
    "成功率(%)",
    "手續費",
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


ITEM_DB = load_item()


def get_materials(item: pd.Series) -> str:
    material_name = ITEM_DB.get(item["_Enchant_Material"])
    material_count = item["_Enchant_Material_Count"]
    return f"{material_name} X{material_count}"


def get_probability_modifier(item: pd.Series) -> str:
    return "否" if item["_Probability_Modifier"] >= 0 else "是"


def load_item_option():
    field_names = [
        "ID",
        "_Name",
        "_Option_Min",
        "_Option_Max",
        "_Enchant_Min",
        "_Enchant_Max",
    ]
    df = pd.read_csv(CSV_PATH / "ITEM_OPTION.csv")
    df = df[field_names]
    data = {}
    for _, row in df.iterrows():
        option_id, *option_data = row
        data[option_id] = option_data
    return data


def export():
    field_names = [
        "ID",
        "_Item_OptionType",
        "_Result",
        "_Material",
        "_Consumption_OP_Min",
        "_Consumption_OP_Max",
        "_Probability_Modifier",
        "_Probability_Max",
        "_charge",
    ]
    df = pd.read_csv(CSV_PATH / f"{LDT_NAME}.csv", low_memory=False)
    # df["_Probability_Modifier"] = df.apply(get_probability_modifier, axis=1)
    df["_Material"] = df.apply(get_materials, axis=1)
    df = df.loc[df["_Item_OptionType"] != 0]
    df = df[field_names]
    # 加載數據
    item_option = load_item_option()
    # 寫入數據
    with open(f"{LDT_NAME}.csv", "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(EXPORT_FIELD_NAMES_IN_CHINIESE)
        for _, row in df.iterrows():
            if item_data := item_option.get(int(row["_Result"])):
                option_name, option_min, option_max, enchant_min, enchant_max = item_data
            writer.writerow(
                [
                    row["ID"],
                    row["_Item_OptionType"],
                    option_name,
                    option_min,
                    option_max,
                    enchant_min,
                    enchant_max,
                    row["_Material"],
                    row["_Consumption_OP_Min"],
                    row["_Consumption_OP_Max"],
                    row["_Probability_Modifier"],
                    row["_Probability_Max"],
                    row["_charge"],
                ]
            )


if __name__ == "__main__":
    export()

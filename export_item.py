from pathlib import Path

import pandas as pd


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"


OPTION_TYPE = {
    1: "職業:",
    2: "性別:",
    3: "使用等級:%d",
    10: "名聲+%d",
    11: "名聲+%d%%",
    14: "力量+%d",
    15: "力量+%d%%",
    18: "幸運+%d",
    19: "幸運+%d%%",
    22: "魔力+%d",
    23: "魔力+%d%%",
    26: "體力 %+d",
    27: "體力+%d%%",
    30: "最大HP %+d",
    31: "最大HP+%d%%",
    34: "最大SP+%d",
    35: "最大SP+%d%%",
    38: "屬性力+%d",
    39: "屬性力+%d%%",
    42: "風屬性+%d",
    43: "風屬性+%d%%",
    46: "火屬性+%d",
    47: "火屬性+%d%%",
    50: "地屬性+%d",
    51: "地屬性+%d%%",
    54: "休息恢復HP+%d",
    55: "休息恢復HP+%d%%",
    58: "休息恢復SP+%d",
    59: "休息恢復SP+%d%%",
    62: "最大攻擊力+%d",
    63: "最大攻擊力+%d%%",
    66: "最小攻擊力+%d",
    67: "最小攻擊力+%d%%",
    70: "水抵抗力+%d",
    71: "水抵抗力+%d%%",
    74: "風抵抗力+%d",
    75: "風抵抗力+%d%%",
    78: "火抵抗力+%d",
    79: "火抵抗力+%d%%",
    82: "地抵抗力+%d",
    83: "地抵抗力+%d%%",
    86: "減少傷害+%d%%",
    87: "減少傷害+%d%%",
    90: "物理最小傷害+%d%%",
    91: "最終物理最小傷害 +%d%%",
    94: "物理最大傷害+%d%%",
    95: "最終物理最大傷害 +%d%%",
    98: "魔法最小傷害+%d%%",
    99: "最終魔法最小傷害 +%d%%",
    102: "魔法最大傷害+%d%%",
    103: "最終魔法最大傷害 +%d%%",
    106: "移動速度+%d%%",
    107: "移動速度+%d%%",
    110: "彈跳力%d%%",
    111: "彈跳力%d%%",
    114: "繩索移動速度+%d%%",
    115: "繩索移動速度+%d%%",
    118: "梯子移動速度+%d%%",
    119: "梯子移動速度+%d%%",
    121: "技能點數+%d",
    124: "獲得經驗值+%d%%",
    125: "獲得經驗值+%d%%",
    128: "獲得錢+%d%%",
    129: "獲得錢+%d%%",
    132: "道具掉落率+%d%%",
    133: "道具掉落率+%d%%",
    136: "屬性發生機率+%d%%",
    137: "屬性發生機率+%d%%",
    140: "物理傷害+%d",
    141: "物理傷害+%d%%",
    144: "物理減少傷害+%d",
    145: "物理減少傷害+%d%%",
    148: "目標物理防禦力減少%d%%",
    149: "目標物理防 禦力減少%d%%",
    152: "跳躍攻擊力+%d",
    153: "跳躍攻擊力+%d%%",
    156: "物理爆擊傷害+%d%%",
    157: "最終物理爆擊傷害 +%d%%",
    158: "物理爆擊率+%d%%",
    159: "物理爆擊率+%d%%",
    162: "魔法爆擊傷害+%d%%",
    163: "最終魔法爆擊傷害 +%d%%",
    164: "魔法爆擊率+%d%%",
    165: "魔法爆擊率+%d%%",
    168: "治癒爆擊恢復量+%d%%",
    169: "治癒爆擊恢復量+%d%%",
    172: "治癒爆擊率+%d%%",
    173: "治癒爆擊率+%d%%",
    176: "物理命中率+%d%%",
    177: "物理命中率+%d%%",
    180: "魔法命中率+%d%%",
    181: "魔法命中率+%d%%",
    184: "物理回避率+%d%%",
    185: "物理回避率+%d%%",
    188: "魔法回避率+%d%%",
    189: "魔法回避率+%d%%",
    192: "物理回擊傷害+%d%%",
    193: "物理回擊傷害+%d%%",
    196: "魔法回擊傷害+%d%%",
    197: "魔法回擊傷害+%d%%",
    200: "物理攻擊等級+%d",
    201: "物理攻擊等級+%d",
    204: "物理攻擊等級[％]+%d",
    205: "物理攻擊等級[％]+%d",
    208: "魔法攻擊等級+%d",
    209: "魔法攻擊等級+%d",
    212: "魔法攻擊等級[％]+%d",
    213: "魔法攻擊等級[％]+%d",
    216: "防禦力+%d",
    217: "防禦力+%d%%",
    218: "屬性力傷害(物理攻擊時)+%d",
    219: "風屬性傷害(物理攻擊時)+%d",
    220: "火屬性傷害(物理攻擊時)+%d",
    221: "地屬性傷害(物理攻擊時)+%d",
    224: "HP治癒量+%d",
    225: "HP治癒量+%d%%",
    228: "SP治癒量+%d",
    229: "SP治癒量+%d%%",
    232: "HP治癒效果+%d%%",
    233: "HP治癒效果+%d%%",
    236: "SP治癒效果+%d%%",
    237: "SP治癒效果+%d%%",
    240: "魔法傷害+%d",
    241: "魔法傷害+%d%%",
    244: "魔法減少傷害+%d",
    245: "魔法減少傷害+%d%%",
    254: "屬性力最小傷害+%d%%",
    255: "屬性力最小傷害+%d%%",
    258: "屬性力最大傷害+%d%%",
    259: "屬性力最大傷害+%d%%",
    262: "風屬性最小傷害+%d%%",
    263: "風屬性最小傷害+%d%%",
    266: "風屬性最大傷害+%d%%",
    267: "風屬性最大傷害+%d%%",
    270: "火屬性最小傷害+%d%%",
    271: "火屬性最小傷害+%d%%",
    274: "火屬性最大傷害+%d%%",
    275: "火屬性最大傷害+%d%%",
    278: "地屬性最小傷害+%d%%",
    279: "地屬性最小傷害+%d%%",
    282: "地屬性最大傷害+%d%%",
    283: "地屬性最大傷害+%d%%",
    284: "物理免疫",
    285: "魔法免疫",
    286: "屬性力免疫",
    287: "風屬性免疫",
    288: "火屬性免疫",
    289: "地屬性免疫",
    292: "目標魔法抵抗力減少+%d%%",
    293: "目標魔法抵抗力減少+%d%%",
    296: "HP治癒量+%d%%",
    297: "HP治癒量+%d%%",
    300: "SP治癒量+%d%%",
    301: "SP治癒量+%d%%",
    302: "毒免疫",
    303: "出血免疫",
    304: "詛咒免疫",
    307: "毒傷害(毒發生時)+%d",
    308: "毒傷害(毒發生時)+%d",
    311: "出血傷害(出血發生時)+%d",
    312: "出血傷害(出血發生時)+%d",
    315: "詛咒傷害(詛咒發生時)+%d",
    316: "詛咒傷害(詛咒發生時)+%d",
    319: "毒傷害(毒發生時)+%d%%",
    320: "毒傷害(毒發生時)+%d%%",
    323: "出血傷害(出血發生時)+%d%%",
    324: "出血傷害(出血發生時)+%d%%",
    327: "詛咒傷害(詛咒發生時)+%d%%",
    328: "詛咒傷害(詛咒發生時)+%d%%",
    331: "毒傷害(毒發生時)%d%%",
    332: "毒傷害(毒發生時)%d%%",
    335: "出血傷害(出血發生時)%d%%",
    336: "出血傷害(出血發生時)%d%%",
    339: "詛咒傷害(詛咒發生時)%d%%",
    340: "詛咒傷害(詛咒發生時)%d%%",
    365: "使用等級%d%%",
    367: "道具套用等級限制 +%d 減少",
    369: "鑲嵌成功率+%d%%",
    384: "製作成功率 +%d%%",
    389: "格鬥點數 +%d%%",
    408: "暈眩抗力 +%0.1F%%",
    409: "睡眠抗力 +%0.1F%%",
    411: "屬性重新分配成功率+%d%%",
    430: "最大 AP+%d",
    431: "最大 CP+%d",
    432: "最大 DP+%d",
    433: "最大 CAP+%d",
    434: "最大 EP+%d",
    435: "最大 BP+%d",
    440: "技能冷卻時間減少+%0.1F%%",
    448: "混亂抗力 +%0.1F%%",
    454: "釣魚附加獲得機率 +%d%%",
    455: "所有能力值 %+d",
    456: "所有能力值 +%d%%",
    457: "水，火，地，風，黑暗屬性 +%d",
    458: "水，火，地，風，黑暗抵抗力 +%d",
    459: "所有屬性最小傷害 +%d%%",
    460: "所有屬性最大傷害 +%d%%",
    461: "物理/魔法最大傷害 +%d%%",
    462: "物理/魔法最小傷害 %+d%%",
    463: "物理/魔法貫穿力 %+d%%",
    464: "物理/魔法爆擊傷害 +%d%%",
    465: "物理/魔法爆擊率 %+d%%",
    466: "物理/魔法命中率 +%d%%",
    470: "黑暗屬性 +%d",
    471: "黑暗屬性 +%d%%",
    474: "黑暗抵抗力 +%d",
    475: "黑暗抵抗力 +%d%%",
    478: "黑暗最小傷害 +%d",
    479: "黑暗最小傷害 +%d%%",
    482: "黑暗最大傷害 +%d",
    483: "黑暗最大傷害 +%d%%",
    484: "黑暗屬性免疫",
    485: "黑暗屬性傷害(物理攻擊時)+%d",
    488: "任務獎勵強化 +%d%%",
    490: "物理最小/最大傷害 +%d%%",
    491: "魔法最小/最大傷害 +%d%%",
    492: "最小/最大攻擊力 +%d",
    493: "最小/最大攻擊力 +%d%%",
    494: "物理/魔法背後攻擊傷害 +%d%%",
    495: "物理/魔法傷害減少 +%d",
    496: "物理/魔法傷害 +%d",
    497: "物理/魔法迴避率 +%d%%",
    498: "物理/魔法免疫",
    499: "特殊計量條 +%d",
    505: "最大元素卡片 +%d",
    510: "最大閃耀卡片 +%d",
    515: "最大暗黑卡片 +%d",
    520: "最大魔力卡片 +%d",
    522: "元素卡片充電減少度 +%0.1F%%",
    523: "閃耀卡片充電減少度 +%0.1F%%",
    524: "暗黑卡片充電減少度 +%0.1F%%",
    525: "魔力卡片充 電減少度 +%0.1F%%",
    526: "所有卡片充電減少度 +%0.1F%%",
    531: "最大 MP +%d",
    532: "彈力 +%d%%",
    533: "最大所有卡片 +%d",
    537: "最大 RP +%d",
    541: "RP 恢復 +%d",
    542: "RP 恢復 +%d%%",
    546: "最大 VP +%d",
    550: "VP 恢復 +%d",
    551: "VP 恢復 +%d%%",
    552: "所有屬性 +%d%%",
    553: "所有抗力 +%d%%",
    566: "一般怪物追加傷害 +%d",
    567: "一般怪物追加傷害 +%d%%",
    570: "BOSS怪物追加傷害 +%d",
    571: "BOSS怪物追加傷害 +%d%%",
    573: "一般怪物支配力 +%0.1F%%",
    574: "BOSS怪物支配力 +%0.1F%%",
    585: "最小/最大傷害 +%d%%",
    586: "武器攻擊力/屬性力 +%d",
    587: "武器攻擊力/屬性力 +%d%%",
    588: "物理/魔法固定傷害 +%d%%",
    590: "物理/魔法最終最小傷害 +%d%%",
    591: "物理/魔法最終最大傷害 +%d%%",
    592: "物理/魔法最終爆擊傷害 +%d%%",
    594: "力量/魔力 +%d",
    595: "力量/魔力 +%d%%",
    596: "防禦力/魔法抗力 +%d",
    597: "防禦力/魔法抗力 +%d%%",
    611: "近距離傷害 +%d",
    612: "近距離傷害 +%d%%",
    614: "所有技能目標數 +%d",
    30001: "強化耐久度:%d",
    30002: "鑲嵌屬性可能等級:%d",
}

EXPORT_FIELD_NAMES = [
    "ID",
    "_Name",
    "_OptionType",
    "_ItemOptions",
]
EXPORT_FIELD_NAMES_IN_CHINIESE = [
    "ID",
    "道具名稱",
    "鑲嵌類型ID",
    "道具屬性",
]


def get_item_options(item: pd.Series):
    item_options = []
    for index in range(1, 10):
        status_type = int(item[f"_StatusType{index}"])
        if status_type != 0:
            status_name = OPTION_TYPE.get(status_type)
            if not status_name:
                raise ValueError(f"{item['ID']} {status_type=}")
            status_value = item[f"_StatusValue{index}"]
            item_options.append(status_name % status_value)
    return "\n".join(item_options)


def export():
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("ITEM_?.csv")])
    # df = df.loc[df["_OptionType"] != 0]
    df["_ItemOptions"] = df.apply(get_item_options, axis=1)
    df = df[EXPORT_FIELD_NAMES]
    df.to_csv(f"ITEM.csv", header=EXPORT_FIELD_NAMES_IN_CHINIESE, index=False, encoding="utf-8")


if __name__ == "__main__":
    export()
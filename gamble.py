from os import name
from pathlib import Path
from typing import Optional, Any

import pandas as pd
from dataclasses import asdict, dataclass, is_dataclass, asdict

import json


TEMP_DIR = Path()

LDT_PATH = Path(TEMP_DIR) / "DATA/LDT"
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"


class DataClassJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


@dataclass
class Item:
    id: int
    name: str
    count: int
    point: int


@dataclass
class Effect:
    id: int


@dataclass
class Gamble:
    id: int
    items: list[Item]
    effects: Optional[list[Effect]] = None

@dataclass
class GambleReward:



def load_gamble():
    pass


def load_item() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Name",
    ]
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_PATH.glob("ITEM_?.csv")])
    df = df[field_names]
    return df

import json
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "output_10_19_2026.json"
with open(RAW_PATH, encoding = "utf-8") as file:
    data = json.load(file)

print(type(data))

if isinstance(data, dict):
    print(data.keys())
elif isinstance(data, list):
    print(len(data))
    if data:
        print(data[0])

DB_PATH = PROJECT_ROOT / "data" / "processed" / "ddr_analysis.db"
connection = sqlite3.connect(DB_PATH)
import json
import sqlite3
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "ddr_analysis.db"
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "output_10_19_2026.json"

# Test Raw Data
with open(RAW_PATH, encoding = "utf-8") as file:
    data = json.load(file)

print(type(data))

if isinstance(data, dict):
    print(data.keys())
elif isinstance(data, list):
    print(len(data))
    if data:
        print(data[0])

# Connect database

def loadJsonToDatabase(data, path):
    connection = sqlite3.connect(path)

    cursor = connection.cursor()
    try:
        for item in data:
            # Populate to Songs
            cursor.execute(
                """
                INSERT OR IGNORE INTO Songs(song_id, song_name) 
                VALUES (?, ?)
                """,
                (item["song_id"], item["song_name"])
            )
            

            # Populate to Charts
            cursor.execute(
                """
                INSERT OR IGNORE INTO Charts(song_id, difficulty, rating) 
                VALUES(?, ?, ?)
                """,
                (item["song_id"], item["difficulty"], item["rating"])
            )

            # Get chart_id first for Score
            cursor.execute("""
                SELECT chart_id
                FROM Charts
                WHERE song_id = ? AND difficulty = ?
            """,
                (item["song_id"], item["difficulty"])
            )
            chart_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO Scores()
                """
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
         connection.close()

import json
import sqlite3
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "ddr_analysis.db"
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "output_10_19_2026.json"

def initializeDatabase(dbPath=DB_PATH):
    """Create the Songs, Charts, and Scores tables if they don't exist.

    Args:
        dbPath (Path): Path to the SQLite database file.
    """

    connection = sqlite3.connect(dbPath)
    try:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute("""
            CREATE TABLE IF NOT EXISTS Songs(
            song_id TEXT Primary KEY,
            song_name TEXT NOT NULL
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS Charts (
                chart_id INTEGER PRIMARY KEY,
                song_id TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                rating INTEGER NOT NULL,
                UNIQUE(song_id, difficulty),
                FOREIGN KEY (song_id) REFERENCES Songs(song_id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS Scores (
                score_id INTEGER PRIMARY KEY,
                chart_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                grade TEXT NOT NULL,
                lamp TEXT NOT NULL,
                flare TEXT,
                flare_skill INTEGER,
                time_uploaded TEXT NOT NULL,
                time_played TEXT,
                UNIQUE(chart_id, time_uploaded),
                FOREIGN KEY (chart_id) REFERENCES Charts(chart_id)
            )
        """)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def loadJsonToDatabase(rawPath=RAW_PATH, dbPath=DB_PATH):
    """Load DDR score data from a JSON file into the SQLite database.

    Existing records that violate database constraints are ignored.

    Args:
        rawPath (Path): Path to the input JSON file.
        dbPath (Path): Path to the SQLite database file.

    Raises:
        FileNotFoundError: If the input JSON file does not exist.
        json.JSONDecodeError: If the input file contains invalid JSON.
        OSError: If the input file cannot be read.
    """
    
    try:
        with open(rawPath, encoding = "utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"File not found: {rawPath}")
        raise

    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {rawPath}")
        raise

    except OSError as e:
        print(f"Error reading file: {e}")
        raise
    
    connection = sqlite3.connect(dbPath)
    connection.execute("PRAGMA foreign_keys = ON")
    
    try:
        for item in data:
            cursor = connection.cursor()

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
            time_played = item.get("time_played") or None
            cursor.execute(
                """
                INSERT OR IGNORE INTO Scores(chart_id, score, grade, lamp, flare, flare_skill, time_uploaded, time_played)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (chart_id, item["score"], item["grade"], item["lamp"], item.get("flare"), item.get("flare_skill"), item["time_uploaded"], time_played)
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
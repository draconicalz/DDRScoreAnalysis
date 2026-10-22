import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "ddr_analysis.db"

def getPBs(limit = 10):
    """Gets the top personal bests.
    
    Args:
        limit (int): How many of the top X personal bests to display
    """
    connection = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        Songs.song_name,
        Charts.difficulty,
        Charts.rating,
        MAX(Scores.score) AS personal_best,
        COUNT(Scores.score_id) AS attempts
    FROM Scores
    JOIN Charts
        ON Scores.chart_id = Charts.chart_id
    JOIN Songs
        ON Charts.song_id = Songs.song_id
    GROUP BY Songs.song_id, Charts.chart_id
    ORDER BY personal_best DESC
    LIMIT ?
    """

    res = connection.execute(query, (limit,)).fetchall()
    connection.close()
    return res

def getRecentPlays(limit = 10):
    """Gets the most recent plays
        
    Args:
        limit (int): How many of the X most recent plays to display
    """

    connection = sqlite3.connect(DB_PATH)
    query = """
    SELECT
        Songs.song_name,
        Charts.difficulty,
        Charts.rating,
        Scores.score,
        Scores.grade,
        Scores.lamp,
        Scores.time_played
    FROM Scores
    JOIN Charts
        ON Scores.chart_id = Charts.chart_id
    JOIN Songs
        ON Charts.song_id = Songs.song_id
    ORDER BY Scores.time_played DESC
    LIMIT ?;
    """

    res = connection.execute(query, (limit,)).fetchall()
    connection.close()
    return res

def getLastUpload():
    """Gets all scores from the last upload"""

    connection = sqlite3.connect(DB_PATH)
    query = """
    SELECT
        Songs.song_name,
        Charts.difficulty,
        Charts.rating,
        Scores.score,
        Scores.grade,
        Scores.lamp,
        Scores.time_uploaded
    FROM Scores
    JOIN Charts
        ON Scores.chart_id = Charts.chart_id
    JOIN Songs
        ON Charts.song_id = Songs.song_id
    WHERE Scores.time_uploaded = (
        SELECT MAX(time_uploaded)
        FROM Scores
    )
    """
    
    res = connection.execute(query).fetchall()
    connection.close()
    return res

def getDifficultyAnalysis():
    """Gets charts played count, average, min, and max score for each difficulty of charts played for that difficulty."""

    connection = sqlite3.connect(DB_PATH)
    query = """
    SELECT
        level,
        COUNT(*) AS chart_count,
        CAST(AVG(personal_best) AS INTEGER) AS average_score,
        MAX(personal_best) AS highest_score,
        MIN(personal_best) AS lowest_score
    FROM (
        SELECT
            Charts.chart_id,
            Charts.rating AS level,
            MAX(Scores.score) AS personal_best
        FROM Scores
        JOIN Charts
            ON Scores.chart_id = Charts.chart_id
        GROUP BY Charts.chart_id
    )
    GROUP BY level
    ORDER BY level;
    """
    
    res = connection.execute(query).fetchall()
    connection.close()
    return res

res = getDifficultyAnalysis()
for row in res:
    print(row)  
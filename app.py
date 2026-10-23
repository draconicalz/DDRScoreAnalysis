import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

from analysis.analyze import getRatingAnalysis

PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "ddr_analysis.db"

st.set_page_config(
    page_title = "DDR Analysis",
    layout = "wide"
)

st.title("DDR Performance Dashboard")
st.write("Explore my personal bests, performance across ratings, and progress.")

if not DB_PATH.exists():
    st.error(f"Database not found: {DB_PATH}")
    st.stop()

res = getRatingAnalysis(14, 19)

df = pd.DataFrame(
    res,
    columns=[
        "level",
        "chart_count",
        "average_score",
        "ceiling",
        "floor"
    ]
)

if df.empty:
    st.warning("No score data found in the database.")
    st.stop()


query = """
SELECT
    (SELECT COUNT(*) FROM Charts) AS charts_recorded,
    (SELECT COUNT(*) FROM Scores) AS score_records,
    (SELECT COUNT(DISTINCT song_id) FROM Charts) AS songs_played,
    (SELECT CAST(AVG(personal_best) AS INTEGER)
     FROM (
         SELECT MAX(score) AS personal_best
         FROM Scores
         GROUP BY chart_id
     )) AS average_personal_best;
"""

with sqlite3.connect(DB_PATH) as connection:
    stats = pd.read_sql_query(query, connection)

charts_recorded = int(stats.loc[0, "charts_recorded"])
score_records = int(stats.loc[0, "score_records"])
songs_played = int(stats.loc[0, "songs_played"])
average_personal_best = stats.loc[0, "average_personal_best"]

col1, col2, col3, col4 = st.columns(4)


col1.metric("Charts recorded", f"{charts_recorded:,}")
col2.metric("Score records", f"{score_records:,}")
col3.metric("Songs played", f"{songs_played:,}")
col4.metric("Average personal best", f"{average_personal_best:,}")

st.subheader("Performance by Chart Rating")

st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Average Personal Best by Level")

st.bar_chart(df, x="level", y="average_score")

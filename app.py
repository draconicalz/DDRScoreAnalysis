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

col1, col2 = st.columns(2)

col1.metric(
    "Charts with recorded scores",
    int(df["chart_count"].sum())
)

col2.metric(
    "Average of level averages",
    f"{df['average_score'].mean():,.0f}"
)

st.subheader("Performance by Chart Rating")

st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Average Personal Best by Level")

st.bar_chart(df, x="level", y="average_score")

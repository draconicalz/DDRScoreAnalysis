# DDR Score Analysis

## Overview

A personal data analysis project focused on exploring performance in Dance Dance Revolution (DDR). The project uses Python, SQL, and SQLite to organize score data and investigate performance patterns across songs, chart difficulties, and scoring metrics.

## Goals

- Build a relational database for storing DDR song, chart, and score data.
- Use SQL to query and organize performance data.
- Use Python to analyze scores and identify performance trends.
- Explore how performance varies across chart difficulties and other available metrics.
- Track personal-best improvements over time as historical data becomes available.

## Technologies

- **Python** — Data processing and analysis
- **SQLite** — Relational database storage
- **SQL** — Data querying and analysis

Additional libraries will be documented as they are introduced.

## Data

The project uses structured DDR score data containing fields such as song IDs, song names, chart difficulties, ratings, scores, grades, lamps, and Flare Skill values.

The initial dataset represents my own personal-best scores. Future data collection may preserve historical personal-best scores to support analysis of improvement over time.

## Database Design

The database is designed around three main entities:

- **Songs** — Song identifiers and names.
- **Charts** — Individual song charts, their difficulties, and ratings.
- **Score History** — Recorded personal-best scores and associated metrics over time.

Primary and foreign keys maintain relationships between songs, charts, and score records.

## Project Structure

```text
DDR Analysis Project/
├── data/processed  # SQLite database
├── data/raw        # Original source data
├── src/            # Data processing and analysis scripts
├── notebooks/      # Exploratory analysis
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup and Usage

Setup instructions will be added as the database schema, data import process, and analysis scripts are implemented.

## Analysis and Results

This section will document findings, visualizations, and insights discovered through SQL queries and Python analysis.

## Future Improvements

- Automate importing new score data.
- Preserve historical personal-best scores.
- Analyze performance across chart difficulties.
- Visualize score changes and improvement over time.

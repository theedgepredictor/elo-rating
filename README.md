# ELO Rating

[![ELO-Rating Data trigger](https://github.com/theedgepredictor/elo-rating/actions/workflows/elo_data_trigger.yaml/badge.svg)](https://github.com/theedgepredictor/elo-rating/actions/workflows/elo_data_trigger.yaml)   [![Build and Deploy React App to Pages](https://github.com/theedgepredictor/elo-rating/actions/workflows/pages_build_and_deploy.yaml/badge.svg)](https://github.com/theedgepredictor/elo-rating/actions/workflows/pages_build_and_deploy.yaml)




## ETL process for Generating Elo Ratings from the ESPN API

This service will:
1. Extract data from the ESPN API
2. Handle attribute selection from the sport event payloads
3. Apply ELO calculations to each event
4. Store ELO for each sport and handle upsert logic as needed
5. Generate updated reports on each elo system for:
    1. Upcoming Event Ratings: ELO ratings for Events in the next 2-7 days
    2. Rest of Season Event Ratings: ELO ratings for the rest of the season (simulates rest of season)
    3. System Evaluation: Performance metrics for the system (All time, This Season, Last Season, ...)
        1. Accuracy, Precision, Recall, F1, AUC, Brier Score, Log Loss, System Score (25 - Brier Score * 100)
        2. Number of records: Number of games making up the evaluation report
        3. Avg Number of Games Played: The average number of games played for a team across the evaluation slice
        4. Avg Points per Game: The average number of points scored for a team across the evaluation slice
        5. Home Win Percentage: The amount of times the home team won for all the games in the evaluation slice
    4. System Settings: Current System Hyperparameters and info about number of teams and number of seasons
    5. Team Ratings: Current ELO Ratings and Rankings for the system


```mermaid
flowchart TB
    subgraph A[Event Collection];
        direction TB;
        A2[Scoreboard API]-->A3[events_runner.py]
        A3[events_runner.py]-->A4[Attribute Selection];
        A4[Attribute Selection]-->A5[data/event/SPORT/SEASON.parquet];
    end;
    subgraph B[Apply Elo];
        direction TB;
        B3[data/event/SPORT/SEASON.parquet]-->B4[elo_runner.py];
        B4[elo_runner.py]-->B5[data/elo/SPORT/SEASON.parquet];
    end;
        subgraph C[Generate Reports];
        direction LR;
        C3[data/elo/SPORT/SEASON.parquet]-->C5[report_runner.py];
        C5[report_runner.py]-->C6[data/reports/SPORT/upcoming_event_ratings.json];
        C5[report_runner.py]-->C7[data/reports/SPORT/restofseason_event_ratings.json];
        C5[report_runner.py]-->C8[data/reports/SPORT/system_evaluation.json];
        C5[report_runner.py]-->C9[data/reports/SPORT/system_settings.json];
        C5[report_runner.py]-->C10[data/reports/SPORT/team_ratings.json];
    end;
A-->B;
B-->C;
```

## Github Pages
[Site Link](https://theedgepredictor.github.io/elo-rating)

Adds visuals for latest reports 

## Active Sports
- Baseball
  - MLB
  - College Baseball
- Basketball
  - NBA
  - Mens College Basketball
- Football
  - NFL
  - College Football
- Hockey
  - NHL
  - Mens College Hockey
- Lacrosse
  - PLL
  - Mens College Lacrosse

## Resources
- [ELO Rating](https://en.wikipedia.org/wiki/Elo_rating_system)
- [538 Elo](https://github.com/fivethirtyeight/nfl-elo-game/tree/master)
- [ESPN Api Hidden Docs](https://gist.github.com/nntrn/ee26cb2a0716de0947a0a4e9a157bc1c)
- [Github Actions Trigger Python Script](https://canovasjm.netlify.app/2020/11/29/github-actions-run-a-python-script-on-schedule-and-commit-changes/)
- [Github Actions Setup Python](https://github.com/actions/setup-python/tree/main)
- [Github Actions Pricing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)

## Future
- ESPN ORM: Map all endpoints to pydantic classes for validation and structure
- Add Soccer Leagues
- Advanced ELO systems: The current system uses a basic static k value, more advanced systems improve upon that by implementing a dynamic k value and a dynamic home_field_advantage factor
- Dockerized runner 
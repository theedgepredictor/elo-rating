import time
import pandas as pd
import datetime
from src.consts import ESPNSportTypes, ELO_HYPERPARAMETERS, START_SEASONS
from src.elo import EloRunner, ELO_SCHEMA
from src.utils import  put_dataframe, get_dataframe, get_seasons_to_update
from src.sport import ESPNSport


def get_active_sports():
    espn_sports = []
    for sport in ESPNSportTypes:
        sport_api = ESPNSport(sport)
        espn_sports.append(sport_api)
    return [espn_sport.sport for espn_sport in espn_sports if espn_sport.is_active]

def run_elo_for_sport(event_root_path,elo_root_path, sport):
    seasons = get_seasons_to_update(elo_root_path, sport)
    print(f'Starting Runner for {sport.value} ({seasons[0]}-{seasons[-1]})...')
    for season in seasons:
        print(f'Making Elo for {sport.value} - {season}')
        try:
            prev_elo_df = pd.concat([get_dataframe(f'{elo_root_path}/{sport.value}/{elo_season}.parquet') for elo_season in list(range(START_SEASONS[sport],season))])
            elo_cols = ['str_event_id', 'season', 'date', 'neutral_site', 'home_team_id', 'home_team_score', 'away_team_id', 'away_team_score','home_elo_pre','away_elo_pre','home_elo_prob','away_elo_prob','home_elo_post','away_elo_post']
        except Exception as e:
            prev_elo_df = pd.DataFrame()
            elo_cols = ['str_event_id', 'season', 'date', 'neutral_site', 'home_team_id', 'home_team_score', 'away_team_id', 'away_team_score']

        df = pd.concat([
            prev_elo_df,
            get_dataframe(f'{event_root_path}/{sport.value}/{season}.parquet')
        ])

        er = EloRunner(
            df=df[elo_cols].rename(columns={'home_team_id': 'home_team_name', 'away_team_id': 'away_team_name'}),
            allow_future=True,
            k=ELO_HYPERPARAMETERS[sport]['k'],
            mean_elo=1505,
            home_field_advantage=ELO_HYPERPARAMETERS[sport]['hfa'],
            width=800,
            preloaded_elos=ELO_HYPERPARAMETERS[sport]['preloaded_elos'] if season == START_SEASONS[sport] else None
        )
        elo_df = er.run_to_date()
        elo_df = elo_df.rename(columns={'home_team_name': 'home_team_id', 'away_team_name': 'away_team_id'})
        elo_df = pd.merge(elo_df, df[['id', 'str_event_id', 'home_team_name', 'away_team_name', 'is_postseason', 'tournament_id', 'is_finished', 'datetime']], on=['str_event_id'])
        elo_df = elo_df.loc[elo_df.season == season]
        put_dataframe(elo_df, f'{elo_root_path}/{sport.value}/{season}.parquet', ELO_SCHEMA)

def main():
    sports = [ESPNSportTypes.COLLEGE_BASKETBALL]#get_active_sports()
    status_reports = {}
    for sport in sports:
        start = time.time()
        try:
            run_elo_for_sport(event_root_path='./data/events',elo_root_path='./data/elo', sport=sport)
            status_reports[sport] = {
                'status':True,
                'execution_time':round(time.time() - start, 2),
                'end_datetime': datetime.datetime.utcnow()
            }
        except Exception as e:
            print('FAILURE')
            print(e)
            status_reports[sport] = {
                'status':False,
                'execution_time':round(time.time() - start, 2),
                'end_datetime': datetime.datetime.utcnow()
            }
    print('')
    print('Elo Pump Status Report')
    print('-' * 110)
    duration = 0
    for key, report in status_reports.items():
        duration = duration + report['execution_time']
        print(f"    {key}: {'PASSED' if report['status'] else 'FAILED'} -- took {report['execution_time']} sec, finished at ({report['end_datetime']}) ")
    print('')
    print(f'Pump took {duration} sec')
    print('-' * 110)

if __name__ == "__main__":
    main()
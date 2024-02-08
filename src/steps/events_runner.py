import time

import pandas as pd
import datetime
from src.consts import ESPNSportTypes, SEASON_GROUPS
from src.utils import create_dataframe, put_dataframe, get_dataframe, get_seasons_to_update, known_missed_date
from src.sport import ESPNSport
from src.event import ESPNEventsAPI


def get_active_sports():
    """
    Get a list of active ESPN sports based on their current status.

    Returns:
        List: List of active sports.
    """
    espn_sports = []
    for sport in ESPNSportTypes:
        sport_api = ESPNSport(sport)
        espn_sports.append(sport_api)
    return [espn_sport.sport for espn_sport in espn_sports if espn_sport.is_active]


def get_valid_team_ids_for_sport_season(sport: ESPNSportTypes, season: int, espn_events_api: ESPNEventsAPI):
    """
    Get valid team IDs for a specific sport and season.

    Args:
        sport (ESPNSportTypes): Type of sport.
        season (int): Season year.
        espn_events_api (ESPNEventsAPI): ESPN Events API object.

    Returns:
        List: List of valid team IDs.
    """
    team_ids = []
    core_sport = sport.value.split('/')[0] + '/leagues/' + sport.value.split('/')[1]
    url = f'http://sports.core.api.espn.com/v2/sports/{core_sport}/seasons/{season}/teams'
    res = espn_events_api.api_request(url + '?limit=500')
    for item in res['items']:
        team_ids.append(int(item['$ref'].replace(url + '/', '').split('?')[0]))
    return team_ids


def run_events_for_sport(root_path: str, sport: ESPNSportTypes, espn_events_api: ESPNEventsAPI):
    """
    Run events retrieval process for a specific sport.

    Args:
        root_path (str): Root path for event data.
        sport (ESPNSportTypes): Type of sport.
        espn_events_api (ESPNEventsAPI): ESPN Events API object.

    Returns:
        None
    """
    seasons = get_seasons_to_update(root_path, sport)

    print(f'Starting Runner for {sport.value} ({seasons[0]}-{seasons[-1]})...')
    for season in seasons:
        team_ids = get_valid_team_ids_for_sport_season(sport, season, espn_events_api)
        espn_sport_obj = ESPNSport(sport=sport, season=season)
        on_days = espn_sport_obj.ondays
        groups = SEASON_GROUPS[sport]
        if groups is not None:
            groups = groups['di']
        if espn_sport_obj.start_date is None:
            print(f'No Data for {sport.value} - {season}...')
            continue

        print(f'Getting Events for {sport.value} - {season}')
        start_date = espn_sport_obj.start_date.strftime('%Y%m%d')
        end_date = espn_sport_obj.end_date.strftime('%Y%m%d')

        fs_df = get_dataframe(f'{root_path}/{sport.value}/{season}.parquet')
        # If the file does not exist refresh else update the dataset with the new data
        if fs_df.shape[0] == 0:
            fs_df = pd.DataFrame()
            dates = f"{start_date}-{end_date}"
            print(f'    Refreshing data from {dates}...')
        else:
            start_date = fs_df.loc[fs_df['is_finished'] == True].datetime.max().strftime('%Y%m%d')
            dates = f"{start_date}-{end_date}"
            print(f'    Updating data from {dates}...')
            on_days = [day for day in on_days if pd.Timestamp(start_date).to_pydatetime() <= day <= pd.Timestamp(end_date).to_pydatetime()]
            fs_df = fs_df.loc[((fs_df.season == season) & (fs_df.is_finished == True) & (fs_df.datetime <= start_date))]

        # Collect all event payloads from api
        events = []
        if len(on_days) == 0:
            print('    No Events Need Updating')
            continue
        missed_dates = []
        for date in on_days:
            try:
                res = espn_events_api.get_events_for_elo(sport, date.strftime('%Y%m%d'), groups=groups)
                events.extend(res)
            except Exception as e:
                print(f"    -- Missed Date {date.strftime('%Y%m%d')} --")
                if date > datetime.datetime.utcnow():
                    print(f'        Missed Date is future date. Scrape will be run up to {date - datetime.timedelta(days=1)}')
                    break
                if not known_missed_date(sport, date):
                    missed_dates.append(date)
        # Add second pass (api timesout on a specific date sometimes. Finishing on_dates and re running missed dates results in less errors)
        for date in missed_dates:
            res = espn_events_api.get_events_for_elo(sport, date.strftime('%Y%m%d'), groups=groups)
            events.extend(res)
        df = create_dataframe(events, espn_events_api.SCHEMA)

        df = df.loc[((df.away_team_id.isin(team_ids)) & (df.home_team_id.isin(team_ids)))]

        df = pd.concat([fs_df, df], ignore_index=True).drop_duplicates(['id'], keep='last')
        df = df.sort_values(['datetime'])

        if season != seasons[-1]:
            df = df.loc[((df.home_team_score.notnull()) & (df.away_team_score.notnull()))]
        df = df.loc[df.season == season]
        put_dataframe(df, f'{root_path}/{sport.value}/{season}.parquet', espn_events_api.SCHEMA)


def main():
    """
    Main function to run events retrieval for specified sports.

    Returns:
        None
    """
    sports = [ESPNSportTypes.COLLEGE_BASKETBALL]  # get_active_sports()
    status_reports = {}
    for sport in sports:
        start = time.time()
        try:
            run_events_for_sport(root_path='./data/events', sport=sport, espn_events_api=ESPNEventsAPI())
            status_reports[sport] = {
                'status': True,
                'execution_time': round(time.time() - start, 2),
                'end_datetime': datetime.datetime.utcnow()
            }
        except Exception as e:
            print('FAILURE')
            print(e)
            status_reports[sport] = {
                'status': False,
                'execution_time': round(time.time() - start, 2),
                'end_datetime': datetime.datetime.utcnow()
            }
    print('')
    print('Events Pump Status Report')
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

import datetime

import numpy as np
import pandas as pd

from src.base_api import ESPNBaseAPI
from src.consts import ESPNSportTypes, ESPNSportSeasonTypes, ESPNEventStatusTypes
from src.utils import name_filter


class ESPNEventsAPI(ESPNBaseAPI):
    """
    ESPN Events API for retrieving sports events information.

    Attributes:
        SCHEMA (dict): Dictionary defining the data schema for events.

    Methods:
        get_scoreboard(sport, dates, limit=1000, groups=None): Retrieve scoreboard data for a specific sport.
        get_events(sport, dates, limit=1000, groups=None): Retrieve events data for a specific sport.
        get_events_for_elo(sport, dates, limit=1000, groups=None): Retrieve events data suitable for Elo calculations.
        _collect_elo_payload(event, name_type='shortDisplayName'): Collect Elo payload for a given event.
        _team_name_validator(name): Validate and filter team names.

    """
    def __init__(self):
        """
        Initialize ESPNEventsAPI.
        """
        super().__init__()
        self.SCHEMA = {
            'id':np.int64,
            'season':np.int32,
            'is_postseason': np.int8,
            'tournament_id':'Int32',
            'is_finished': np.int8,
            'neutral_site': np.int8,
            'home_team_id':np.int32,
            'home_team_score':'Int32',
            'away_team_id':np.int32,
            'away_team_score':'Int32',
        }

    def get_scoreboard(self, sport: ESPNSportTypes, dates, limit=1000, groups=None):
        """
        Retrieve scoreboard data for a specific sport.

        Args:
            sport (ESPNSportTypes): Type of sport.
            dates: Dates for events.
            limit (int): Limit of events to retrieve.
            groups: Groups for events.

        Returns:
            dict: API response containing scoreboard data.
        """
        url = f"{self._base_url}/{sport.value}/scoreboard?dates={dates}&limit={limit}"
        if groups is not None:
            url=f"{url}&groups={groups}"
        return self.api_request(url)

    def get_events(self, sport: ESPNSportTypes, dates, limit=1000, groups=None):
        """
        Retrieve events data for a specific sport.

        Args:
            sport (ESPNSportTypes): Type of sport.
            dates: Dates for events.
            limit (int): Limit of events to retrieve.
            groups: Groups for events.

        Returns:
            list: List of events data.
        """
        res = self.get_scoreboard(sport, dates, limit, groups)
        if res is None:
            return []
        return res['events']

    def get_events_for_elo(self, sport: ESPNSportTypes, dates, limit=1000, groups=None):
        """
        Retrieve events data suitable for Elo calculations.

        Args:
            sport (ESPNSportTypes): Type of sport.
            dates: Dates for events.
            limit (int): Limit of events to retrieve.
            groups: Groups for events.

        Returns:
            list: List of events data suitable for Elo calculations.
        """
        events = self.get_events(sport, dates, limit, groups)
        elos = []
        if sport == ESPNSportTypes.COLLEGE_HOCKEY:
            name_type = 'displayName'
        elif sport == ESPNSportTypes.COLLEGE_LACROSSE:
            name_type = 'abbreviation'
        else:
            name_type = 'shortDisplayName'
        for event in events:
            elo = self._collect_elo_payload(event,sport,name_type)
            if elo is not None:
                elos.append(elo)
        return elos


    def _collect_elo_payload(self,event,sport:ESPNSportTypes, name_type='shortDisplayName'):
        """
        Collect Elo payload for a given event.

        Args:
            event: Event data.
            name_type (str): Type of team name to use.

        Returns:
            dict: Elo payload for the event.
        """
        id = event['id']
        try:
            date = pd.Timestamp(event['date']).to_pydatetime()
            # Select only regular and post season games
            if event['season']['type'] not in [
                ESPNSportSeasonTypes.REG.value, #2
                ESPNSportSeasonTypes.POST.value #3
            ] and sport != ESPNSportTypes.SOCCER_EPL:
                return None
            is_postseason = int(event['season']['type']) == ESPNSportSeasonTypes.POST.value #3

            if 'status' not in event:
                print('-'*30)
                print(f'Missing Status: {id}')
                print(event)
                print('-' * 30)
                is_finished = date < pd.Timestamp(datetime.datetime.now(tz=datetime.timezone.utc)).to_pydatetime()
            else:
                # Select games that are scheduled or final
                if int(event['status']['type']['id']) not in [
                    ESPNEventStatusTypes.SCHEDULED.value,  # 1
                    ESPNEventStatusTypes.FINAL.value,  # 3
                ]:
                    return None
                is_finished = int(event['status']['type']['id']) == ESPNEventStatusTypes.FINAL.value #3

            # Handle Home and Away team selection from competitors
            if event['competitions'][0]['competitors'][0]['homeAway'] == 'home':
                home_team_idx = 0
                away_team_idx = 1
            else:
                home_team_idx = 0
                away_team_idx = 1

            home_team = event['competitions'][0]['competitors'][home_team_idx]
            away_team = event['competitions'][0]['competitors'][away_team_idx]
            try:
                home_score = int(home_team['score']) if home_team['score'] is not None else None
                away_score = int(away_team['score']) if away_team['score'] is not None else None
            except Exception as e:
                home_score = None
                away_score = None

            record = {
                'id':id,
                'str_event_id':None,
                'season':event['season']['year'],
                'is_postseason': is_postseason,
                'tournament_id': event['competitions'][0]['tournamentId'] if 'tournamentId' in event['competitions'][0] else None,
                'is_finished':is_finished,
                'neutral_site': event['competitions'][0]['neutralSite'],
                'date':date.strftime('%Y-%m-%d'),
                'datetime':date,
                'home_team_id':home_team['id'],
                'home_team_name':self._team_name_validator(home_team['team'][name_type]),
                'home_team_score':home_score if is_finished else None,
                'away_team_id':away_team['id'],
                'away_team_name':self._team_name_validator(away_team['team'][name_type]),
                'away_team_score':away_score if is_finished else None,
            }
            record['str_event_id'] = f"{record['datetime'].strftime('%Y%m%d')}_{record['home_team_name']}_{record['away_team_name']}"
            return record
        except Exception as e:
            print(f'Event Parsing Error: {id}')
            print(e)
            return None

    def _team_name_validator(self, name):
        """
        Validate and filter team names.

        Args:
            name: Team name.

        Returns:
            str: Validated and filtered team name.
        """
        if name[0] == '[' and name[-1] == ']':
            name = name[1:].split(',')[0]
        return name_filter(name)



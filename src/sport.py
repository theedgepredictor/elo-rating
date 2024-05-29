import datetime

from src.base_api import ESPNBaseAPI
from src.consts import ESPNSportTypes, SEASON_START_MONTH, SEASON_GROUPS, ESPNSportSeasonTypes


class ESPNSport(ESPNBaseAPI):
    """
    A reference to an ESPN Sport Object.

    Attributes:
        sport (ESPNSportTypes): Type of sport.
        espn_core_name (str): ESPN core name for the sport.
        is_college_sport (bool): True if the sport is related to college.
        date (datetime.datetime): Date for the sport.
        season: Season for the sport.
        start_date (datetime.datetime): Start date of the sport season.
        end_date (datetime.datetime): End date of the sport season.
        is_active (bool): True if the sport season is currently active.
        ondays: List of datetime objects representing specific days in the season.
        groups: Season groups for the sport.

    Methods:
        _find_year_for_season(league, date=None): Find the year for the season based on league and date.
        _get_calendar(): Retrieve the calendar information for the sport season.

    """
    def __init__(
            self,
            sport: ESPNSportTypes,
            date: datetime.datetime = datetime.datetime.utcnow(),
            season=None
    ):
        """
        Initialize ESPNSport.

        Args:
            sport (ESPNSportTypes): Type of sport.
            date (datetime.datetime): Date for the sport.
            season: Season for the sport (default is None).
        """
        super().__init__()
        self.sport = sport
        self.espn_core_name = sport.value.split('/')[0] + '/leagues/' + sport.value.split('/')[1]
        self.is_college_sport = 'college' in sport.value
        self.date = date
        self.season = self._find_year_for_season(sport, date) if season is None else season

        self.start_date = None
        self.end_date = None
        self.is_active = None
        self.ondays = None
        if not (self.season == 2005 and self.sport == ESPNSportTypes.NHL):
            self._get_calendar()
        self.groups = SEASON_GROUPS[self.sport]

    def _find_year_for_season(self, league: ESPNSportTypes, date: datetime.datetime = None):
        """
        Find the year for the season based on league and date.

        Args:
            league (ESPNSportTypes): Type of sport.
            date (datetime.datetime): Date for the sport (default is None).

        Returns:
            int: Year for the season.
        """
        if date is None:
            today = datetime.datetime.utcnow()
        else:
            today = date
        if league not in SEASON_START_MONTH:
            raise ValueError(f'"{league}" league cannot be found!')
        start = SEASON_START_MONTH[league]['start']
        wrap = SEASON_START_MONTH[league]['wrap']
        if wrap and start - 1 <= today.month <= 12:
            return today.year + 1
        elif not wrap and start == 1 and today.month == 12:
            return today.year + 1
        elif not wrap and not start - 1 <= today.month <= 12:
            return today.year - 1
        else:
            return today.year

    def _get_calendar(self):
        """
        Retrieve the calendar information for the sport season.
        """
        try:
            reg_res = self.api_request(f"{self._core_url}/{self.espn_core_name}/seasons/{self.season}/types/{ESPNSportSeasonTypes.REG.value}")
            post_res = self.api_request(f"{self._core_url}/{self.espn_core_name}/seasons/{self.season}/types/{ESPNSportSeasonTypes.POST.value}")
            if 'startDate' in reg_res:
                self.start_date = datetime.datetime.strptime(reg_res['startDate'], '%Y-%m-%dT%H:%MZ')
                if post_res is not None:
                    self.end_date = datetime.datetime.strptime(post_res['endDate'], '%Y-%m-%dT%H:%MZ') if 'endDate' in post_res else datetime.datetime.strptime(reg_res['endDate'], '%Y-%m-%dT%H:%MZ')
                else:
                    self.end_date = datetime.datetime.strptime(reg_res['endDate'], '%Y-%m-%dT%H:%MZ')
                self.is_active = self.start_date <= self.date <= self.end_date
                res = self.api_request(f"{self._core_url}/{self.espn_core_name}/calendar/ondays?dates={self.season}")
                if 'dates' in res['eventDate']:
                    self.ondays = [datetime.datetime.strptime(date, '%Y-%m-%dT%H:%MZ') for date in res['eventDate']['dates'] if self.start_date <= datetime.datetime.strptime(date, '%Y-%m-%dT%H:%MZ') <= self.end_date]
        except Exception as e:
            if self.sport == ESPNSportTypes.SOCCER_EPL:
                res = self.api_request(f"{self._core_url}/{self.espn_core_name}/seasons/{self.season}/types/1/calendar/ondays")
            else:
                res = self.api_request(f"{self._core_url}/{self.espn_core_name}/calendar/ondays?dates={self.season}")
            if res is None:
                print('No Date Response for '+self.sport.value)
                self.is_active = False
                return 
            if 'startDate' not in res:
                raise e
            self.start_date = datetime.datetime.strptime(res['startDate'], '%Y-%m-%dT%H:%MZ')
            self.end_date = datetime.datetime.strptime(res['endDate'], '%Y-%m-%dT%H:%MZ')
            self.is_active = self.start_date <= self.date <= self.end_date
            if 'dates' in res['eventDate']:
                self.ondays = [datetime.datetime.strptime(date, '%Y-%m-%dT%H:%MZ') for date in res['eventDate']['dates']]

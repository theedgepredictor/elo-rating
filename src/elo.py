import math

import numpy as np
import pandas as pd

from src.utils import df_rename_fold, is_pandas_none

initial_load_columns = ['str_event_id','season','date','neutral_site','home_team_name','home_team_score','away_team_name','away_team_score']
upsert_load_columns = initial_load_columns + ['home_elo_pre','away_elo_pre','home_elo_prob','away_elo_prob','home_elo_post','away_elo_post']

ELO_SCHEMA = {

}

class EloRunner:
    '''
    Base Elo Runner for any 1v1 event
    - df: pd.DataFrame() -> Can be either initial or upsert dataset states (df must follow the initial or upsert column format or it will not work (small price to pay for auto elo))
    - mode: str -> upsert or refresh
    - allow_future: bool -> Include events that are upcoming in the simulation (Denoted by None in away_team_score and home_team_score)
    - k: int -> K Factor. Higher K = higher rating chance
    - mean_elo: int -> Average rating score
    - home_field_advantage: int -> Home team is awarded this many points to their base rating
    - width: int -> lower and upper bounds of elo ratings (mean_elo-width, mean_elo+width)
    - revert_percentage: float -> new season/year distance towards mean_elo (common is 1/3 revert back to mean)
    '''
    def __init__(
            self,df:pd.DataFrame(),
            mode:str='refresh',
            allow_future:bool=False,
            k:int=20,
            mean_elo:int=1500,
            home_field_advantage:int=100,
            width:int=400,
            revert_percentage:float = 1.0 / 3,
            preloaded_elos = None
    ):
        self.runner_df = pd.DataFrame()
        self.current_elos = {}
        self.games = []
        self.mode = mode
        self.allow_future = allow_future
        self._k = k
        self._mean_elo = mean_elo
        self._hfa = home_field_advantage
        self._width = width
        if revert_percentage > 1 or revert_percentage < 0:
            raise Exception('Invalid revert percentage')
        self._revert_percentage = revert_percentage

        self._load_state(df.copy(),preloaded_elos=preloaded_elos)

    def _load_state(self,df,preloaded_elos=None):
        if len(df.columns) == len(initial_load_columns):
            df = df[initial_load_columns].copy()
        elif len(df.columns) == len(upsert_load_columns):
            df = df[upsert_load_columns].copy()
        else:
            raise Exception('Invalid DataFrame Dimensions')

        if 'home_elo_pre' in df.columns and 'away_elo_pre' in df.columns:
            if len(df.loc[~df.home_elo_pre.isnull()].home_elo_pre.values) > 0 and len(df.loc[~df.away_elo_pre.isnull()].away_elo_pre.values) > 0:
                self.mode = 'upsert'
        else:
            df['home_elo_pre'] = None
            df['away_elo_pre'] = None
            df['home_elo_prob'] = None
            df['away_elo_prob'] = None
            df['home_elo_post'] = None
            df['away_elo_post'] = None

        df = df[upsert_load_columns]
        df['date'] = pd.to_datetime(df['date'])
        df['neutral_site'] = df['neutral_site'].astype(int)

        if self.mode == 'refresh':
            unique_teams = list(set(list(df.home_team_name.values) + list(df.away_team_name.values)))
            self.current_elos = dict(zip(unique_teams,[self._mean_elo for _ in unique_teams]))
            df = df.sort_values(['season','date'])
            self.runner_df = df
        else:
            # Get latest elo for each team
            # Determine games we need to run and save that subset as the runner_df
            latest_df = df.loc[df.season == df.season.max()]
            latest_df = df_rename_fold(latest_df, 'away_', 'home_')
            team_latest_elos = latest_df.sort_values('date').groupby('team')['team_elo_pre'].first().reset_index()
            self.current_elos = dict(zip(list(team_latest_elos.team.values),list(team_latest_elos.team_elo_pre.values)))
            df = df.sort_values(['season','date'])
            self.runner_df = df

        if preloaded_elos is not None:
            self.current_elos = {**self.current_elos, **preloaded_elos}

    def run_to_date(self):
        current_season = self.runner_df.season.min()
        for row in self.runner_df.itertuples(index=False):
            if row.season != current_season:
                self.rating_reset()
                current_season = row.season
            dict_row = {
                'str_event_id':row.str_event_id,
                'season':row.season,
                'date':row.date,
                'neutral_site':row.neutral_site,
                'home_team_name':row.home_team_name,
                'home_team_score':row.home_team_score,
                'away_team_name': row.away_team_name,
                'away_team_score':row.away_team_score,
                'home_elo_pre':self.current_elos[row.home_team_name],
                'home_elo_prob':row.home_elo_prob,
                'home_elo_post':row.home_elo_post,
                'away_elo_pre': self.current_elos[row.away_team_name],
                'away_elo_prob': row.away_elo_prob,
                'away_elo_post':row.away_elo_post,
            }
            elo_game = EloGame(**dict_row)
            res = elo_game.sim(
                k=self._k,
                hfa=self._hfa,
                width=self._width,
                allow_future=self.allow_future
            )
            if res['home_elo_post'] is not None and res['away_elo_post'] is not None:
                self.current_elos[row.home_team_name] = res['home_elo_post']
                self.current_elos[row.away_team_name] = res['away_elo_post']
            self.games.append(res)
        return pd.DataFrame(self.games)[upsert_load_columns]


    def rating_reset(self):
        """
            Regression towards the mean
        """
        team_names, elos = zip(*self.current_elos.items())
        diff_from_mean = np.array(elos) - self._mean_elo # Default mean or actual list mean?
        elos -= diff_from_mean * (self._revert_percentage)
        self.current_elos = dict(zip(team_names,elos))



class EloGame:
    def __init__(
            self,
            str_event_id:str,
            season:int,
            date:pd.Timestamp,
            neutral_site:int,
            home_team_name:str,
            home_team_score:int,
            away_team_name:str,
            away_team_score:int,
            home_elo_pre:float=1500.0,
            home_elo_prob:float=None,
            home_elo_post:float=None,
            away_elo_pre:float=1500.0,
            away_elo_prob:float=None,
            away_elo_post:float=None,
    ):
        self.str_event_id = str_event_id
        self.season=season
        self.date=date
        self.neutral_site=neutral_site
        self.home_team_name=home_team_name
        self.home_team_score=home_team_score
        self.away_team_name=away_team_name
        self.away_team_score=away_team_score
        self.home_elo_pre = home_elo_pre
        self.home_elo_prob = home_elo_prob
        self.home_elo_post = home_elo_post
        self.away_elo_pre = away_elo_pre
        self.away_elo_prob = away_elo_prob
        self.away_elo_post = away_elo_post

    def update_elo(self, k=15,hfa=5,width=400,allow_future=False):
        try:
            # get expected home score
            elo_diff = self.home_elo_pre - self.away_elo_pre + (0 if self.neutral_site == 1 else hfa)
            expected_home_shift = 1.0 / (math.pow(10.0, (-elo_diff/width)) + 1.0)
            expected_away_shift = 1.0 / (math.pow(10.0, (elo_diff/width)) + 1.0)

            if is_pandas_none(self.away_team_score):
                self.away_team_score = None
            if is_pandas_none(self.home_team_score):
                self.home_team_score = None
            if self.away_team_score is None and self.home_team_score is None:
                if allow_future:
                    margin = expected_home_shift - expected_away_shift
                else:
                    return expected_home_shift,expected_away_shift,None, None
            else:
                margin = self.home_team_score - self.away_team_score

            if margin > 0:
                # shift of 1 for a win
                true_res = 1
            elif margin < 0:
                # shift of 0 for a loss
                true_res = 0
            else:
                # shift of 0.5 for a tie
                true_res = 0.5

            # Margin of victory multiplier calculation
            abs_margin = abs(margin)
            mult = math.log(max(abs_margin, 1) + 1.0) * (2.2 / (1.0 if true_res == 0.5 else ((elo_diff if true_res == 1.0 else -elo_diff) * 0.001 + 2.2)))

            # multiply difference of actual and expected score by k value and adjust home rating
            shift = (k * mult) * (true_res - expected_home_shift)
            new_home_elo = self.home_elo_pre + shift

            # repeat these steps for the away team
            # away shift is inverse of home shift
            new_away_elo = self.away_elo_pre - shift

            # return a tuple
            return expected_home_shift, expected_away_shift, new_home_elo, new_away_elo
        except ZeroDivisionError as e:
            print (e)
        except Exception as e:
            print (e)

    def sim(self,k=40,hfa=100,width=400,allow_future=False):
        self.home_elo_prob, self.away_elo_prob,self.home_elo_post, self.away_elo_post = self.update_elo(k=k,hfa=hfa,width=width,allow_future=allow_future)
        return self.__dict__


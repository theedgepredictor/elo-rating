import re
import pandas as pd
from src.consts import ESPNSportTypes, SEASON_START_MONTH
import datetime
import os
from typing import List
import pyarrow as pa

def clean_string(s):
    if isinstance(s, str):
        return re.sub("[^A-Za-z0-9 ]+", '', s)
    else:
        return s
def re_braces(s):
    if isinstance(s, str):
        return re.sub("[\(\[].*?[\)\]]", "", s)
    else:
        return s
def name_filter(s):
    if isinstance(s, str):
      # Adds space to words that
      s = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', s)
      if 'Mary' not in s and ' State' not in s:
          s=s.replace(' St', ' State')
      if 'University' not in s:
          s=s.replace('Univ', 'University')
      if 'zz' in s or 'zzz' in s or 'zzzz' in s:
          s = s.replace('zzzz','').replace('zzz','').replace('zz','')
      s = clean_string(s)
      s = re_braces(s)
      s = str(s)
      s = s.replace(' ', '').lower()
      return s
    else:
      return s

def get_dataframe(path: str, columns: List=None):
    try:
        return pd.read_parquet(path, dtype_backend='numpy_nullable', columns=columns)
    except Exception as e:
        print(e)
        return pd.DataFrame()

def put_dataframe(df: pd.DataFrame, path: str, schema: dict):
    key, file_name = path.rsplit('/',1)
    if file_name.split('.')[1] != 'parquet':
        raise Exception("Invalid Filetype for Storage (Supported: 'parquet')")
    os.makedirs(key, exist_ok=True)
    for column, dtype in schema.items():
        df[column] = df[column].astype(dtype)
    df.to_parquet(f"{key}/{file_name}", schema=pa.Schema.from_pandas(df))

def create_dataframe(obj, schema: dict):
    df = pd.DataFrame(obj)
    for column, dtype in schema.items():
        df[column] = df[column].astype(dtype)
    return df

def df_rename_fold(df, t1_prefix, t2_prefix):
    '''
    The reverse of a df_rename_pivot
    Fold two prefixed column types into one generic type
    Ex: away_team_id and home_team_id -> team_id
    '''
    try:
        t1_all_cols = [i for i in df.columns if t2_prefix not in i]
        t2_all_cols = [i for i in df.columns if t1_prefix not in i]

        t1_cols = [i for i in df.columns if t1_prefix in i]
        t2_cols = [i for i in df.columns if t2_prefix in i]
        t1_new_cols = [i.replace(t1_prefix, '') for i in df.columns if t1_prefix in i]
        t2_new_cols = [i.replace(t2_prefix, '') for i in df.columns if t2_prefix in i]

        t1_df = df[t1_all_cols].rename(columns=dict(zip(t1_cols, t1_new_cols)))
        t2_df = df[t2_all_cols].rename(columns=dict(zip(t2_cols, t2_new_cols)))

        df_out = pd.concat([t1_df, t2_df]).reset_index().drop(columns='index')
        return df_out
    except Exception as e:
        print("--df_rename_fold-- " + str(e))
        print(f"columns in: {df.columns}")
        print(f"shape: {df.shape}")
        return df
    


def is_pandas_none(val):
    return str(val) in ["nan", "None", "", "none", " ", "<NA>", "NaT", "NaN"]

def find_year_for_season(league: ESPNSportTypes, date: datetime.datetime = None):
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
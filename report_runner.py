import json
import os
import time
import pandas as pd
import numpy as np
import datetime

from scipy.stats import gamma

from src.consts import ESPNSportTypes, ELO_HYPERPARAMETERS, START_SEASONS
from src.utils import get_dataframe, find_year_for_season, df_rename_fold
from src.sport import ESPNSport
from sklearn.metrics import brier_score_loss, log_loss, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score


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
    return [espn_sport.sport for espn_sport in espn_sports if espn_sport.is_active and espn_sport.sport != ESPNSportTypes.SOCCER_EPL]


def classification_evaluation(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Evaluate classification metrics for binary or multiclass classification.

    Parameters:
    - y_true (numpy.ndarray): True labels.
    - y_pred (numpy.ndarray): Predicted probabilities or class labels.

    Returns:
    dict: Dictionary containing classification metrics.
    """
    y_true = np.array(y_true).ravel()
    if set(y_true) == {0, 1} or len(list(set(y_true))) <= 2:
        # Binary classification
        y_true_binary = y_true.astype(bool)
        brier_score = brier_score_loss(y_true_binary, y_pred)
        y_pred_binary = (y_pred > 0.5).astype(int)
        accuracy = accuracy_score(y_true_binary, y_pred_binary)
        precision = precision_score(y_true_binary, y_pred_binary)
        recall = recall_score(y_true_binary, y_pred_binary)
        f1 = f1_score(y_true_binary, y_pred_binary)
        if len(list(set(y_true))) < 2:
            roc_auc = None
            log_loss_score = None
        else:
            roc_auc = roc_auc_score(y_true_binary, y_pred_binary)
            log_loss_score = log_loss(y_true_binary, y_pred)
        error = y_pred.round(2) - y_true_binary
        my_score = ((25 - (100 * error)).sum() / len(y_true_binary)).round(2)
    else:
        # Multiclass classification
        y_true_multiclass = y_true
        log_loss_score = log_loss(y_true_multiclass, y_pred)
        y_pred_multiclass = np.argmax(y_pred, axis=1)
        accuracy = accuracy_score(y_true_multiclass, y_pred_multiclass)
        precision = precision_score(y_true_multiclass, y_pred_multiclass, average='weighted')
        recall = recall_score(y_true_multiclass, y_pred_multiclass, average='weighted')
        f1 = f1_score(y_true_multiclass, y_pred_multiclass, average='weighted')
        roc_auc = None
        brier_score = None
        my_score = None

    return {
        'system_accuracy': accuracy,
        'system_precision': precision,
        'system_recall': recall,
        'system_f1': f1,
        'system_auc': roc_auc,
        'system_brier_score': brier_score,
        'system_log_loss': log_loss_score,
        'system_score': my_score,
        'system_records': len(y_true),
    }


def regression_evaluation(y_pred, y_true) -> dict:
    """
    Evaluate regression metrics.

    Parameters:
    - y_true (numpy.ndarray): True value.
    - y_pred (numpy.ndarray): Predicted value.

    Returns:
    dict: Dictionary containing regression metrics.
    """
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {
        'system_mse': mse,
        'system_mae': mae,
        'system_mape': mape,
        'system_r2': r2,
        'system_records': len(y_true),
    }


def trim_outliers(data):
    # Remove Outliers
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data >= lower_bound) & (data <= upper_bound)]


def generate_gamma_distribution(elo_df):
    '''
    Generate gamma distribution of historical point differentials.
    We trim outliers in the point difs, take the absolute value of the
    point difs and fit the points to a gamma distribution.
    :param elo_df:
    :return:
    '''
    scores = elo_df.loc[((elo_df.is_finished == 1))]
    records = scores.shape[0] if scores.shape[0] < 10000 else 10000
    scores = scores[-records:][['away_team_score', 'home_team_score']]
    dif_scores = scores.away_team_score - scores.home_team_score
    dif_scores_no_outliers = trim_outliers(dif_scores)
    dif_scores_no_outliers = dif_scores_no_outliers.abs()
    shape, loc, scale = gamma.fit(dif_scores_no_outliers)
    return shape, loc, scale


def calculate_spread_from_probability(prob, shape, loc, scale):
    '''
    Function to convert a probability to a given spread based on the fit gamma
    distribution hyperparameters
    :param prob:
    :param shape:
    :param loc:
    :param scale:
    :return:
    '''
    probability = abs(0.50 - prob) * 2
    ppf_value = gamma.ppf(probability, shape, loc, scale)
    adjusted_ppf_value = (ppf_value - 1) * 2
    return -adjusted_ppf_value if prob > 0.5 else adjusted_ppf_value


def generate_system_settings(elo_df: pd.DataFrame, sport: ESPNSportTypes) -> dict:
    """
    Generate system settings based on Elo DataFrame and sport.

    Parameters:
    - elo_df (pd.DataFrame): DataFrame containing Elo ratings.
    - sport (str): Sport identifier.

    Returns:
    dict: System settings.
    """
    system_settings = {
        'k': ELO_HYPERPARAMETERS[sport]['k'],
        'hfa': ELO_HYPERPARAMETERS[sport]['hfa'],
        'mean_elo': 1505,
        'system_name': f"{sport.value.split('/')[1].upper()} ELO System",
        'number_of_teams': len(elo_df['team_id'].unique()),
        'number_of_seasons': len(elo_df['season'].unique()),
        'lastupdated': datetime.datetime.utcnow().isoformat(),
    }
    return system_settings


def generate_system_evaluation(eval_df: pd.DataFrame, sport: ESPNSportTypes, season='ALL'):
    """
    Generate system evaluation metrics based on evaluation DataFrame and season.

    Parameters:
    - eval_df (pd.DataFrame): DataFrame containing evaluation data.
    - season (str | int): Season identifier.

    Returns:
    dict: System evaluation metrics.
    """
    if season != 'ALL':
        eval_df = eval_df.loc[eval_df.season == season].copy()

    if eval_df.shape[0] == 0:
        print(f'No Records for {sport.value}-{season} for Evaluation')
        return None

    # Classification Evaluation
    y_true = eval_df['result']
    y_pred = eval_df['home_elo_prob']
    classification_metrics = classification_evaluation(y_true, y_pred)

    # Regression Evaluation
    y_true = eval_df['point_dif']
    y_pred = eval_df['elo_spread']
    regression_metrics = regression_evaluation(y_true, y_pred)
    metrics = {
        **classification_metrics,
        **regression_metrics
    }

    folded_df = df_rename_fold(eval_df[['season', 'home_team_name', 'home_team_score', 'away_team_name', 'away_team_score']], 'away_', 'home_')
    num_games = folded_df.groupby(['team_name', 'season']).agg({
        'team_score': 'count'  # Count number of attribute
    })
    metrics['avg_number_of_games_played'] = num_games.reset_index().groupby('season')['team_score'].mean().mean()
    avg_score = folded_df.groupby(['team_name', 'season']).agg({
        'team_score': 'mean'  # Avg number of attribute
    })
    metrics['avg_points_per_game'] = avg_score.reset_index().groupby('season')['team_score'].mean().mean()

    hw = eval_df.loc[eval_df.neutral_site == 0].copy()
    hw['home_is_winner'] = hw['home_team_score'] > hw['away_team_score']
    hw = hw.groupby(['season']).agg({'home_is_winner': 'sum', 'id': 'count'}).reset_index()
    hw['perc'] = hw['home_is_winner'] / hw['id']
    metrics['home_win_percentage'] = hw['perc'].mean()
    return metrics


def generate_system_evaluations(eval_df: pd.DataFrame, sport: ESPNSportTypes, season) -> dict:
    """
    Generate system evaluations for multiple seasons.

    Parameters:
    - eval_df (pd.DataFrame): DataFrame containing evaluation data.
    - season (str): Current season identifier.

    Returns:
    dict: System evaluations for different seasons.
    """
    eval_seasons = ['ALL', season, season - 1, season - 2]
    evals = {}
    for eval_season in eval_seasons:
        evals[eval_season] = generate_system_evaluation(eval_df, sport, eval_season)
    return {
        'evaluations': evals,
        'lastupdated': datetime.datetime.utcnow().isoformat(),
    }


def get_upcoming_short_shift_for_sport(sport):
    sport_shifts = {
        ESPNSportTypes.COLLEGE_BASKETBALL: 2,
        ESPNSportTypes.COLLEGE_FOOTBALL: 7,
        ESPNSportTypes.COLLEGE_BASEBALL: 2,
        ESPNSportTypes.COLLEGE_HOCKEY: 7,
        ESPNSportTypes.COLLEGE_LACROSSE: 7,
        ESPNSportTypes.NBA: 2,
        ESPNSportTypes.NFL: 14,
        ESPNSportTypes.MLB: 2,
        ESPNSportTypes.NHL: 2,
        ESPNSportTypes.PLL: 7,
        ESPNSportTypes.SOCCER_EPL: 7,
    }
    return sport_shifts[sport]


def generate_event_rating(elo_df: pd.DataFrame, sport: ESPNSportTypes, short_shift=False, played=False):
    """
    Generate event ratings based on Elo DataFrame and sport.

    Parameters:
    - elo_df (pd.DataFrame): DataFrame containing Elo ratings.
    - sport (str): Sport identifier.

    Returns:
    list: List of event ratings.
    """
    report_cols = [
        'id',
        'datetime',
        'neutral_site',
        'is_postseason',
        'home_team_name',
        'home_team_id',
        'away_team_name',
        'away_team_id',
        'home_elo_pre',
        'away_elo_pre',
        'elo_diff',
        'elo_spread',
        'home_elo_prob',
        'away_elo_prob',
        'home_elo_post',
        'away_elo_post',
        'tournament_id',
        'str_event_id',
        'season'
    ]

    if played:
        report_cols = report_cols + ['result','point_dif','home_team_score','away_team_score']

    upcoming_elo_df = elo_df.loc[elo_df.is_finished == played].sort_values(['datetime'])
    if short_shift:
        if played:
            cutoff_datetime = pd.Timestamp(datetime.datetime.utcnow() - datetime.timedelta(days=get_upcoming_short_shift_for_sport(sport))).strftime('%Y-%m-%d')
            upcoming_elo_df = upcoming_elo_df.loc[upcoming_elo_df.datetime >= cutoff_datetime].sort_values(['datetime'],ascending=[False])
            if upcoming_elo_df.shape[0] == 0:
                return None
        else:
            cutoff_datetime = pd.Timestamp(datetime.datetime.utcnow() + datetime.timedelta(days=get_upcoming_short_shift_for_sport(sport))).strftime('%Y-%m-%d')
            upcoming_elo_df = upcoming_elo_df.loc[upcoming_elo_df.datetime <= cutoff_datetime]
            if upcoming_elo_df.shape[0] == 0:
                return None
    return json.loads(upcoming_elo_df[report_cols].to_json(orient='records', date_format='iso'))


def generate_event_ratings(elo_df: pd.DataFrame, sport: ESPNSportTypes) -> dict:
    """
    Generate event ratings based on Elo DataFrame and sport.

    Parameters:
    - elo_df (pd.DataFrame): DataFrame containing Elo ratings.
    - sport (str): Sport identifier.

    Returns:
    dict: Event ratings.
    """
    event_ratings = {
        'events': generate_event_rating(elo_df, sport),
        'lastupdated': datetime.datetime.utcnow().isoformat(),
    }
    return event_ratings


def generate_upcoming_events_ratings(elo_df: pd.DataFrame, sport: ESPNSportTypes) -> dict:
    """
    Generate event ratings based on Elo DataFrame and sport.

    Parameters:
    - elo_df (pd.DataFrame): DataFrame containing Elo ratings.
    - sport (str): Sport identifier.

    Returns:
    dict: Event ratings.
    """
    event_ratings = {
        'events': generate_event_rating(elo_df, sport, short_shift=True),
        'lastupdated': datetime.datetime.utcnow().isoformat(),
    }
    return event_ratings

def generate_previous_events_ratings(elo_df: pd.DataFrame, sport: ESPNSportTypes) -> dict:
    """
    Generate event ratings based on Elo DataFrame and sport.

    Parameters:
    - elo_df (pd.DataFrame): DataFrame containing Elo ratings.
    - sport (str): Sport identifier.

    Returns:
    dict: Event ratings.
    """
    event_ratings = {
        'events': generate_event_rating(elo_df, sport, short_shift=True, played=True),
        'lastupdated': datetime.datetime.utcnow().isoformat(),
    }
    return event_ratings


def generate_team_rating(folded_elo_df: pd.DataFrame) -> list:
    """
    Generate team ratings based on folded Elo DataFrame.

    Parameters:
    - folded_elo_df (pd.DataFrame): Folded DataFrame containing Elo ratings.

    Returns:
    list: List of team ratings.
    """
    current_ratings_df = folded_elo_df.loc[folded_elo_df.is_finished == 1].groupby('team_id').nth(-1).sort_values(['elo_post'], ascending=False)
    current_ratings_df = current_ratings_df.drop(columns=['is_finished', 'elo_pre']).rename(columns={'elo_post': 'elo_rating', 'datetime': 'lastupdated'})
    current_ratings_df = current_ratings_df.drop_duplicates('team_name')  # Sometimes ESPN has multiple ids for one team so check name too
    current_ratings_df = current_ratings_df.loc[current_ratings_df.season >= current_ratings_df.season.max() - 1]
    current_ratings_df['rank'] = [i + 1 for i in range(current_ratings_df.shape[0])]
    return json.loads(current_ratings_df[['id', 'team_name', 'rank', 'elo_rating', 'season', 'lastupdated']].to_json(orient='records', date_format='iso'))


def generate_team_ratings(folded_elo_df: pd.DataFrame) -> dict:
    """
    Generate team ratings based on folded Elo DataFrame.

    Parameters:
    - folded_elo_df (pd.DataFrame): Folded DataFrame containing Elo ratings.

    Returns:
    dict: Team ratings.
    """
    team_ratings = {
        'teams': generate_team_rating(folded_elo_df),
        'lastupdated': datetime.datetime.utcnow().isoformat(),
    }
    return team_ratings


def run_reports_for_sport(elo_root_path: str, report_root_path: str, sport: ESPNSportTypes):
    """
    Run Elo calculations for a specific sport and update Elo ratings.

    Args:
        event_root_path (str): Root path for event data.
        elo_root_path (str): Root path for Elo data.
        sport (ESPNSportTypes): Type of sport.

    Returns:
        None
    """
    current_season = find_year_for_season(sport)
    seasons = list(range(START_SEASONS[sport], current_season + 1))
    elo_df = pd.concat([get_dataframe(f'{elo_root_path}/{sport.value}/{season}.parquet') for season in seasons], ignore_index=True)
    elo_df['result'] = elo_df['home_team_score'] > elo_df['away_team_score']
    elo_df['point_dif'] = elo_df.away_team_score - elo_df.home_team_score

    # Generate Gamma Distribution for calculating spreads from probabilities
    elo_df['elo_diff'] = (elo_df['home_elo_pre'] + (elo_df['neutral_site'] == 0) * ELO_HYPERPARAMETERS[sport]['hfa']) - elo_df['away_elo_pre']
    if sport in [ESPNSportTypes.SOCCER_EPL]:
        shape, loc, scale = generate_gamma_distribution(elo_df.loc[elo_df.is_finished == 1].sort_values(['datetime']))
        elo_df['elo_spread'] = [calculate_spread_from_probability(prob, shape, loc, scale) for prob in elo_df.home_elo_prob.values]
    else:
        if sport == ESPNSportTypes.COLLEGE_LACROSSE:
            adj_k = ELO_HYPERPARAMETERS[sport]['k'] * 1.75
        elif sport == ESPNSportTypes.PLL:
            adj_k = ELO_HYPERPARAMETERS[sport]['k'] * 1.85
        elif sport == ESPNSportTypes.COLLEGE_HOCKEY:
            adj_k = ELO_HYPERPARAMETERS[sport]['k'] * 3
        elif sport == ESPNSportTypes.NHL:
            adj_k = ELO_HYPERPARAMETERS[sport]['k'] * 2.45
        elif sport == ESPNSportTypes.COLLEGE_BASEBALL:
            adj_k = ELO_HYPERPARAMETERS[sport]['k'] * 2.5
        elif sport == ESPNSportTypes.MLB:
            adj_k = ELO_HYPERPARAMETERS[sport]['k'] * 2.5
        else:
            adj_k = ELO_HYPERPARAMETERS[sport]['k']

        elo_df['elo_spread'] = - elo_df['elo_diff'] / adj_k

    event_ratings = generate_event_ratings(elo_df, sport)
    upcoming_event_ratings = generate_upcoming_events_ratings(elo_df, sport)
    previous_event_ratings = generate_previous_events_ratings(elo_df, sport)
    shift = 2 if len(seasons) > 5 else 0
    eval_df = elo_df.loc[((elo_df.is_finished == 1) & (elo_df.season >= START_SEASONS[sport] + shift))].copy()
    del elo_df

    evaluations = generate_system_evaluations(eval_df, sport, current_season)

    folded_elo_df = df_rename_fold(eval_df[['id', 'season', 'datetime', 'is_finished', 'neutral_site', 'home_team_name', 'away_team_name', 'home_team_id', 'away_team_id', 'home_elo_pre', 'away_elo_pre', 'home_elo_post', 'away_elo_post']], 'away_', 'home_').sort_values('datetime')
    team_ratings = generate_team_ratings(folded_elo_df)

    system_settings = generate_system_settings(folded_elo_df, sport)

    endpoints = {
        'system_settings': system_settings,
        'team_ratings': team_ratings,
        'restofseason_event_ratings': event_ratings,
        'upcoming_event_ratings': upcoming_event_ratings,
        'previous_event_ratings': previous_event_ratings,
        'system_evaluation': evaluations,
    }

    # Create the directory if it doesn't exist
    os.makedirs(f'{report_root_path}/{sport.value}', exist_ok=True)

    # Write JSON files for each endpoint
    for endpoint_name, data in endpoints.items():
        with open(f'{report_root_path}/{sport.value}/{endpoint_name}.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)


def main():
    """
    Main function to run Elo calculations for specified sports.

    Returns:
        None
    """
    sports = [sport for sport in ESPNSportTypes if sport != ESPNSportTypes.SOCCER_EPL]
    status_reports = {}
    for sport in sports:
        start = time.time()
        try:
            run_reports_for_sport(elo_root_path='./data/elo', report_root_path='./data/reports', sport=sport)
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

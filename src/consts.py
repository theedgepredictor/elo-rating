from enum import Enum

######################################
# Sport Consts
######################################

class ESPNSportTypes(Enum):
    COLLEGE_BASKETBALL = 'basketball/mens-college-basketball'
    COLLEGE_FOOTBALL = 'football/college-football'
    COLLEGE_BASEBALL = 'baseball/college-baseball'
    COLLEGE_HOCKEY = 'hockey/mens-college-hockey'
    COLLEGE_LACROSSE = 'lacrosse/mens-college-lacrosse'
    NBA = 'basketball/nba'
    NFL = 'football/nfl'
    MLB = 'baseball/mlb'
    NHL = 'hockey/nhl'
    PLL = 'lacrosse/pll'
    SOCCER_EPL = 'soccer/eng.1' #NOT WORKING YET

class ESPNSportSeasonTypes(Enum):
    PRE = 1
    REG = 2
    POST = 3
    OFF = 4

SEASON_GROUPS = {
    ESPNSportTypes.COLLEGE_BASKETBALL: {
        'dii/diii':51,
        'di':50
    },
    ESPNSportTypes.COLLEGE_FOOTBALL: {
        'dii/diii':35,
        'di':90
    },

    ESPNSportTypes.COLLEGE_BASEBALL: {
        'di':26,
    },

    ESPNSportTypes.COLLEGE_HOCKEY: None,
    ESPNSportTypes.COLLEGE_LACROSSE: None,
    ESPNSportTypes.NBA: None,
    ESPNSportTypes.NFL: None,
    ESPNSportTypes.MLB: None,
    ESPNSportTypes.NHL: None,
    ESPNSportTypes.PLL: None,
    ESPNSportTypes.SOCCER_EPL: None,
}

SEASON_START_MONTH = {
    ESPNSportTypes.COLLEGE_BASKETBALL: {'start': 10, 'wrap': True},
    ESPNSportTypes.COLLEGE_FOOTBALL: {'start': 7, 'wrap': False},
    ESPNSportTypes.COLLEGE_BASEBALL: {'start': 1, 'wrap': False},
    ESPNSportTypes.COLLEGE_HOCKEY: {'start': 10, 'wrap': True},
    ESPNSportTypes.COLLEGE_LACROSSE: {'start': 1, 'wrap': False},
    ESPNSportTypes.NBA: {'start': 10, 'wrap': True},
    ESPNSportTypes.NFL: {'start': 9, 'wrap': False},
    ESPNSportTypes.MLB: {'start': 4, 'wrap': False},
    ESPNSportTypes.NHL: {'start': 10, 'wrap': True},
    ESPNSportTypes.PLL: {'start': 6, 'wrap': True},
    ESPNSportTypes.SOCCER_EPL: {'start': 8, 'wrap': False},
}

START_SEASONS = {
    ESPNSportTypes.COLLEGE_BASKETBALL: 2002,
    ESPNSportTypes.COLLEGE_FOOTBALL: 2002,
    ESPNSportTypes.COLLEGE_BASEBALL: 2015,
    ESPNSportTypes.COLLEGE_HOCKEY: 2005,
    ESPNSportTypes.COLLEGE_LACROSSE: 2008,
    ESPNSportTypes.NBA: 2000,
    ESPNSportTypes.NFL: 2002,
    ESPNSportTypes.MLB: 2000,
    ESPNSportTypes.NHL: 2000,
    ESPNSportTypes.PLL: 2022,
    ESPNSportTypes.SOCCER_EPL: 2003,
}


###############################################
# Event Consts
###############################################

class ESPNEventStatusTypes(Enum):
    SCHEDULED = 1
    IN_PROGRESS = 2
    FINAL = 3
    CANCELED = 5
    POSTPONED = 6

###############################################
# Elo Consts
###############################################

NFL_PRELOADED_ELOS = {
    1: 1378.04505736,
    2: 1370.2091015,
    29: 1350.35861283,
    3: 1625.32863848,
    4: 1380.04974226,
    5: 1435.01085703,
    11: 1441.21550067,
    22: 1394.57826681,
    6: 1389.7316795,
    7: 1517.3717214,
    8: 1328.5625712,
    9: 1627.36948839,
    30: 1480.70572893,
    12: 1473.44547412,
    15: 1533.66432859,
    16: 1461.32761689,
    18: 1491.60506307,
    17: 1672.63692769,
    19: 1496.21678316,
    20: 1544.84290764,
    10: 1548.05255981,
    21: 1668.68533629,
    23: 1635.39333726,
    13: 1585.14511287,
    14: 1708.61047359,
    33: 1598.47028852,
    24: 1389.79962434,
    26: 1508.20616702,
    25: 1588.58379811,
    27: 1569.45041313,
    28: 1542.4067468,
    34: 1300,  # New Team
}

ELO_HYPERPARAMETERS = {
    ESPNSportTypes.COLLEGE_BASKETBALL: {
        'k':30,
        'hfa':100,
        'preloaded_elos':None
    },
    ESPNSportTypes.COLLEGE_FOOTBALL: {
        'k':25,
        'hfa':62,
        'preloaded_elos':None
    },

    ESPNSportTypes.COLLEGE_BASEBALL: {
        'k':10,
        'hfa':30,
        'preloaded_elos':None
    },
    ESPNSportTypes.COLLEGE_HOCKEY: {
        'k':10,
        'hfa':5,
        'preloaded_elos':None
    },

    ESPNSportTypes.COLLEGE_LACROSSE: {
        'k':30,
        'hfa':20,
        'preloaded_elos':None
    },
    ESPNSportTypes.NBA: {
        'k':30,
        'hfa':100,
        'preloaded_elos':None
    },
    ESPNSportTypes.NFL: {
        'k':25,
        'hfa':75,
        'preloaded_elos':NFL_PRELOADED_ELOS
    },
    ESPNSportTypes.MLB: {
        'k':5,
        'hfa':50,
        'preloaded_elos':None
    },
    ESPNSportTypes.NHL:{
        'k':8,
        'hfa':25,
        'preloaded_elos':None
    },
    ESPNSportTypes.PLL: {
        'k':30,
        'hfa':20,
        'preloaded_elos':None
    },
    ESPNSportTypes.SOCCER_EPL: {
        'k':30,
        'hfa':100,
        'preloaded_elos':None
    },
}


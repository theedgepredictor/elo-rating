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
    SOCCER_EPL = 'soccer/eng.1'

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

    ESPNSportTypes.COLLEGE_LACROSSE: {
        'di':90
    },
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
    ESPNSportTypes.SOCCER_EPL: {'start': 8, 'wrap': True},
}

START_SEASONS = {
    ESPNSportTypes.COLLEGE_BASKETBALL: 2002,
    ESPNSportTypes.COLLEGE_FOOTBALL: 2002,
    ESPNSportTypes.COLLEGE_BASEBALL: 2015,
    ESPNSportTypes.COLLEGE_HOCKEY: 2005,
    ESPNSportTypes.COLLEGE_LACROSSE: 2007,
    ESPNSportTypes.NBA: 2000,
    ESPNSportTypes.NFL: 2002,
    ESPNSportTypes.MLB: 2000,
    ESPNSportTypes.NHL: 2000,
    ESPNSportTypes.PLL: 2022,
    ESPNSportTypes.SOCCER_EPL: 2001,
}


###############################################
# Event Consts
###############################################

class ESPNEventStatusTypes(Enum):
    SCHEDULED = 1
    IN_PROGRESS = 2
    FINAL = 3
    POSTPONED = 6

###############################################
# Elo Consts
###############################################

ELO_HYPERPARAMETERS = {
    ESPNSportTypes.COLLEGE_BASKETBALL: {
        'k':30,
        'hfa':100
    },
    ESPNSportTypes.COLLEGE_FOOTBALL: {
        'k':19,
        'hfa':62
    },

    ESPNSportTypes.COLLEGE_BASEBALL: {
        'k':16,
        'hfa':30
    },
    ESPNSportTypes.COLLEGE_HOCKEY: {
        'k':30,
        'hfa':100
    },

    ESPNSportTypes.COLLEGE_LACROSSE: {
        'k':30,
        'hfa':100
    },
    ESPNSportTypes.NBA: {
        'k':30,
        'hfa':100
    },
    ESPNSportTypes.NFL: {
        'k':20,
        'hfa':65
    },
    ESPNSportTypes.MLB: {
        'k':30,
        'hfa':100
    },
    ESPNSportTypes.NHL:{
        'k':30,
        'hfa':100
    },
    ESPNSportTypes.PLL: {
        'k':30,
        'hfa':100
    },
    ESPNSportTypes.SOCCER_EPL: {
        'k':30,
        'hfa':100
    },
}
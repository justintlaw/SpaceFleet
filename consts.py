# value to clear the console in a print method
CLEAR_CONSOLE = '\033[H\033[J'

# name for each fleet
USER_FLEET_NAME = 'User Fleet'
ENEMY_FLEET_NAME = 'Enemy Fleet'

# -1 is used to indicate invalid input for integers
INVALID_INTEGER = -1

# adjust the right title in the progress bar
TITLE_RIGHT_ADJUST = 65

# Adjust text
LEFT_ALIGN_METER = 20
LEFT_ALIGN = 15
RIGHT_ADJUST = 50

# constants for difficulty multipliers
DIFFICULTY = {
    'easy': 0.25,
    'medium': 0.50,
    'hard': 0.75,
    'very hard': 1.00,
    'impossible': 1.25
}

# constants for ship indexes
CARRIER_INDEX = 0
DESTROYER_INDEX = 1
CORVETTE_INDEX = 2
FIGHTER_INDEX = 3

# dictionaries for variants of ships (these are created by the programmer)
CARGO_SHIP = {
    'name': 'Cargo Ship',
    'hit_points': 1000,
    'speed': 40,
    'cost': 1000
}

CARRIER = {
    'name': 'Carrier',
    'hit_points': 2000,
    'num_guns': 16,
    'num_missiles': 4,
    'speed': 10,
    'cost': 100000
}

DESTROYER = {
    'name': 'Destroyer',
    'hit_points': 1000,
    'num_guns': 15,
    'num_missiles': 8,
    'speed': 25,
    'cost': 30000
}

CORVETTE = {
    'name': 'Corvette',
    'hit_points': 300,
    'num_guns': 10,
    'num_missiles': 4,
    'speed': 40,
    'cost': 10000
}

FIGHTER = {
    'name': 'Fighter',
    'hit_points': 50,
    'num_guns': 4,
    'num_missiles': 2,
    'speed': 60,
    'cost': 1500
}
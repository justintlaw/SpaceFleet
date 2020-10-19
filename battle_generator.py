# contains all the code to run a battle
from ships import *
from consts import *
import random

# helper function to ensure each carrier has at least 5 fighters
def has_fighters(oFleet):
    for carrier in oFleet.carriers:
        if len(carrier.fighters) < 5:
            return False
    return True            

# helper function to determine which ship is elegible to be added to the fleet
def get_ship_index(fRequiredStrength, fEnemyFleetStrength, bHasCarrierSpace, oFleet):
    dPossibleShips = {
        'Carrier': 0,
        'Destroyer': 1,
        'Corvette': 2,
        'Fighter': 3
    }

    lstIndexes = []

    carrierStrength = get_strength(CARRIER['hit_points'], CARRIER['num_guns'], CARRIER['num_missiles'])
    destroyerStrength = get_strength(DESTROYER['hit_points'], DESTROYER['num_guns'], DESTROYER['num_missiles'])

    # a carrier or destroyer is possible if it adding it will not
    # increase the fleet strength above half the required strength
    # if (len(oFleet.carriers) == 5):
    #     print('gotcha')
    if (carrierStrength + fEnemyFleetStrength) < (fRequiredStrength / 1.25) and (len(oFleet.carriers) < Fleet.MAX_CARRIER_SHIPS) and has_fighters(oFleet):
        lstIndexes.append(dPossibleShips['Carrier'])
    else:
        # if a carrier cannot be added, increase the odds a fighter is added
        if bHasCarrierSpace:
            lstIndexes.append(dPossibleShips['Fighter'])
    if (destroyerStrength + fEnemyFleetStrength) < (fRequiredStrength / 1.25) and (len(oFleet.destroyers) < Fleet.MAX_DESTROYER_SHIPS):
        lstIndexes.append(dPossibleShips['Destroyer'])
    # a fighter is possible if a carrier exists and has space
    if bHasCarrierSpace:
        lstIndexes.append(dPossibleShips['Fighter'])
    # a corvette is always possible
    lstIndexes.append(dPossibleShips['Corvette'])

    return lstIndexes[random.randrange(0, len(lstIndexes))]

# helper function to get strength of potential variants of ships
def get_strength(iHitPoints, iNumGuns, iNumMissiles):
    iStrength = iNumGuns * MilitaryShip.GUN_DAMAGE + iNumMissiles * MilitaryShip.MISSILE_DAMAGE
    return iStrength

# # returns a new carrier based on a dictionary of values
# def create_carrier(dictCarrier, oFleet):
#     return Carrier(CARRIER['name'], CARRIER['speed'], CARRIER['hit_points'], oFleet, CARRIER['num_guns'], CARRIER['num_missiles'])

# # returns a new fighter based on a dictionary of values and a carrier
# def create_fighter(dictFighter, oCarrier, oFleet):
#     return Fighter(FIGHTER['name'], FIGHTER['speed'], FIGHTER['hit_points'], oFleet, FIGHTER['num_guns'], FIGHTER['num_missiles'], oCarrier)

# # returns a new destroyer based on a dictionary of values
# def create_destroyer(dictDestroyer, oFleet):
#     return Destroyer(DESTROYER['name'], DESTROYER['speed'], DESTROYER['hit_points'], oFleet, DESTROYER['num_guns'], DESTROYER['num_missiles'])

# # returns a new corvette based on a dictionary of values
# def create_corvette(dictCorvette, oFleet):
#     return Corvette(CORVETTE['name'], CORVETTE['speed'], CORVETTE['hit_points'], oFleet, CORVETTE['num_guns'], CORVETTE['num_missiles'])

# def run_battle(oUserFleet):

# generate an enemy fleet with a given difficulty
def generate_enemy_fleet(oUserFleet, fDifficultyRatio):
    fUserStrength = oUserFleet.get_strength()
    # strength the fleet must hit to meet the difficulty level
    fRequiredStrength = fUserStrength * fDifficultyRatio
    fEnemyFleetStrength = 0

    oEnemyFleet = Fleet(ENEMY_FLEET_NAME)

    # add ships to the enemy fleet until it passes the required strength
    while(fEnemyFleetStrength < fRequiredStrength):
        carrierStrength = get_strength(CARRIER['hit_points'], CARRIER['num_guns'], CARRIER['num_missiles'])
        destroyerStrength = get_strength(DESTROYER['hit_points'], DESTROYER['num_guns'], DESTROYER['num_missiles'])
        corvetteStrength = get_strength(CORVETTE['hit_points'], CORVETTE['num_guns'], CORVETTE['num_missiles'])
        fighterStrength = get_strength(FIGHTER['hit_points'], FIGHTER['num_guns'], FIGHTER['num_missiles'])

        # get the index of the ship to add
        iShipIndex = get_ship_index(fRequiredStrength, fEnemyFleetStrength, oEnemyFleet.carrier_has_space(), oEnemyFleet)

        # add a carrier
        if iShipIndex == CARRIER_INDEX:
            oEnemyFleet.carriers.append(create_carrier(CARRIER, oEnemyFleet))
            # append a few fighters to a carrier by default
            for iCounter in range (0, 1):
                oEnemyFleet.carriers[len(oEnemyFleet.carriers) - 1].fighters.append(create_fighter(FIGHTER, oEnemyFleet.carriers[len(oEnemyFleet.carriers) - 1], oEnemyFleet))

        # add a destroyer
        elif iShipIndex == DESTROYER_INDEX:
            oEnemyFleet.destroyers.append(create_destroyer(DESTROYER, oEnemyFleet))
        
        # add a fighter
        elif iShipIndex == FIGHTER_INDEX:
            iCarrierIndex = oEnemyFleet.get_available_carrier_index()
            oEnemyFleet.carriers[iCarrierIndex].fighters.append(create_fighter(FIGHTER, oEnemyFleet.carriers[iCarrierIndex], oEnemyFleet))
        
        # add a corvette
        elif iShipIndex == CORVETTE_INDEX:
            oEnemyFleet.corvettes.append(create_corvette(CORVETTE, oEnemyFleet))
        
        # update the enemy fleet strength
        fEnemyFleetStrength = oEnemyFleet.get_strength()

    return oEnemyFleet

# oUserFleet = Fleet('User Fleet')

# oUserFleet.carriers.append(create_carrier(CARRIER, oUserFleet))
# oUserFleet.carriers.append(create_carrier(CARRIER, oUserFleet))

# for i in oUserFleet.carriers:
#     for j in range(10):
#         i.fighters.append(create_fighter(FIGHTER, i, oUserFleet))
# for i in range(4):
#     oUserFleet.destroyers.append(create_destroyer(DESTROYER, oUserFleet))
# for i in range (8):
#     oUserFleet.corvettes.append(create_corvette(CORVETTE, oUserFleet))

# print(oUserFleet.get_info())

# oEnemyFleet = generate_enemy_fleet(oUserFleet, HARD)

# print(oEnemyFleet.get_info())

# print('User Strength: ' + str(oUserFleet.get_strength()))
# print('Enemy Strength: ' + str(oEnemyFleet.get_strength()))
# print(str(float(
#     oEnemyFleet.get_strength() / oUserFleet.get_strength())))
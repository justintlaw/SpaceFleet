from battle_generator import *
# from index import player
from consts import *
from colors import Colors
import time
import os

# oUserFleet = Fleet(USER_FLEET_NAME)

# oUserFleet.carriers.append(create_carrier(CARRIER, oUserFleet))
# oUserFleet.carriers.append(create_carrier(CARRIER, oUserFleet))

# for i in oUserFleet.carriers:
#     for j in range(10):
#         i.fighters.append(create_fighter(FIGHTER, i, oUserFleet))
# for i in range(4):
#     oUserFleet.destroyers.append(create_destroyer(DESTROYER, oUserFleet))
# for i in range (8):
#     oUserFleet.corvettes.append(create_corvette(CORVETTE, oUserFleet))

# # create an enemy fleet
# oEnemyFleet = generate_enemy_fleet(oUserFleet, DIFFICULTY['very hard'])

# def run_battle(oUserFleet, oEnemyFleet):
#     print('test')

class BattleQueue:
    def __init__(self, oUserFleet, oEnemyFleet):

        # initiate gun and missiles queue lists
        self.gun_queue = []
        self.missile_queue = []

        # objects of user and enemy fleet
        self.user_fleet = oUserFleet
        self.enemy_fleet = oEnemyFleet

        # hold a list of ships for each party
        self.user_ships = []
        self.enemy_ships = []

        # populate the list of user ships
        for carrier in oUserFleet.carriers:
            self.user_ships.append(carrier)
        for destroyer in oUserFleet.destroyers:
            self.user_ships.append(destroyer)
        for corvette in oUserFleet.corvettes:
            self.user_ships.append(corvette)
        for carrier in oUserFleet.carriers:
            for fighter in carrier.fighters:
                self.user_ships.append(fighter)
        
        # populate the list of enemy ships
        for carrier in oEnemyFleet.carriers:
            self.enemy_ships.append(carrier)
        for destroyer in oEnemyFleet.destroyers:
            self.enemy_ships.append(destroyer)
        for corvette in oEnemyFleet.corvettes:
            self.enemy_ships.append(corvette)
        for carrier in oEnemyFleet.carriers:
            for fighter in carrier.fighters:
                self.enemy_ships.append(fighter)

        # get the maximum amount of guns and missiles for each fleet
        self.user_max_guns = oUserFleet.get_max_guns()
        self.user_max_missiles = oUserFleet.get_max_missiles()
        self.enemy_max_guns = oEnemyFleet.get_max_guns()
        self.enemy_max_missiles = oEnemyFleet.get_max_missiles()

        # detemine the overall highest amount of guns and missiles
        self.overall_max_guns = self.user_max_guns
        self.overall_max_missiles = self.user_max_missiles

        if self.overall_max_guns < self.enemy_max_guns:
            self.overall_max_guns = self.enemy_max_guns
        if self.overall_max_missiles < self.enemy_max_missiles:
            self.overall_max_missiles = self.enemy_max_missiles

        # append all ships to gun queues
        # append carriers to the gun queue
        iMaxCarriers = len(oUserFleet.carriers)
        if len(oUserFleet.carriers) < len(oEnemyFleet.carriers):
            iMaxCarriers = len(oEnemyFleet.carriers)
        for iCount in range(0, iMaxCarriers):
            if iCount < len(oUserFleet.carriers):
                for iCount2 in range(0, CARRIER['num_guns']):
                    self.gun_queue.append(oUserFleet.carriers[iCount])
            if iCount < len(oEnemyFleet.carriers):
                for iCount2 in range(0, CARRIER['num_guns']):
                    self.gun_queue.append(oEnemyFleet.carriers[iCount])

        # destroyers
        iMaxDestroyers = len(oUserFleet.destroyers)
        if len(oUserFleet.destroyers) < len(oEnemyFleet.destroyers):
            iMaxDestroyers = len(oEnemyFleet.destroyers)
        for iCount in range(0, iMaxDestroyers):
            if iCount < len(oUserFleet.destroyers):
                for iCount2 in range(0, DESTROYER['num_guns']):
                    self.gun_queue.append(oUserFleet.destroyers[iCount])
            if iCount < len(oEnemyFleet.destroyers):
                for iCount2 in range(0, DESTROYER['num_guns']):
                    self.gun_queue.append(oEnemyFleet.destroyers[iCount])
        
        # corvettes
        iMaxCorvettes = len(oUserFleet.corvettes)
        if len(oUserFleet.corvettes) < len(oEnemyFleet.corvettes):
            iMaxCorvettes = len(oEnemyFleet.corvettes)
        for iCount in range(0, iMaxCorvettes):
            if iCount < len(oUserFleet.corvettes):
                for iCount2 in range(0, CORVETTE['num_guns']):
                    self.gun_queue.append(oUserFleet.corvettes[iCount])
            if iCount < len(oEnemyFleet.corvettes):
                for iCount2 in range(0, CORVETTE['num_guns']):
                    self.gun_queue.append(oEnemyFleet.corvettes[iCount])

        # create a list of user fighters
        lstUserFighters = []
        for carrier in oUserFleet.carriers:
            for fighter in carrier.fighters:
                for iCount2 in range(0, FIGHTER['num_guns']):
                    lstUserFighters.append(fighter)
        # create a list of enemy fighters
        lstEnemyFighters = []
        for carrier in oEnemyFleet.carriers:
            for fighter in carrier.fighters:
                for iCount2 in range(0, FIGHTER['num_guns']):
                    lstEnemyFighters.append(fighter)
        # get max fighters between the two
        iMaxFighters = len(lstUserFighters)
        if len(lstUserFighters) < len(lstEnemyFighters):
            iMaxFighters = len(lstEnemyFighters)
        # append each fighter to the queue
        for iCount in range(0, iMaxFighters):
            if iCount < len(lstUserFighters):
                self.gun_queue.append(lstUserFighters[iCount])
            if iCount < len(lstEnemyFighters):
                self.gun_queue.append(lstEnemyFighters[iCount])    

        # append all ships to missile queues
        # append carriers to the gun queue
        iMaxCarriers = len(oUserFleet.carriers)
        if len(oUserFleet.carriers) < len(oEnemyFleet.carriers):
            iMaxCarriers = len(oEnemyFleet.carriers)
        for iCount in range(0, iMaxCarriers):
            if iCount < len(oUserFleet.carriers):
                for iCount2 in range(0, CARRIER['num_missiles']):
                    self.missile_queue.append(oUserFleet.carriers[iCount])
            if iCount < len(oEnemyFleet.carriers):
                for iCount2 in range(0, CARRIER['num_missiles']):
                    self.missile_queue.append(oEnemyFleet.carriers[iCount])

        # destroyers
        iMaxDestroyers = len(oUserFleet.destroyers)
        if len(oUserFleet.destroyers) < len(oEnemyFleet.destroyers):
            iMaxDestroyers = len(oEnemyFleet.destroyers)
        for iCount in range(0, iMaxDestroyers):
            if iCount < len(oUserFleet.destroyers):
                for iCount2 in range(0, DESTROYER['num_missiles']):
                    self.missile_queue.append(oUserFleet.destroyers[iCount])
            if iCount < len(oEnemyFleet.destroyers):
                for iCount2 in range(0, DESTROYER['num_missiles']):
                    self.missile_queue.append(oEnemyFleet.destroyers[iCount])
        
        # corvettes
        iMaxCorvettes = len(oUserFleet.corvettes)
        if len(oUserFleet.corvettes) < len(oEnemyFleet.corvettes):
            iMaxCorvettes = len(oEnemyFleet.corvettes)
        for iCount in range(0, iMaxCorvettes):
            if iCount < len(oUserFleet.corvettes):
                for iCount2 in range(0, CORVETTE['num_missiles']):
                    self.missile_queue.append(oUserFleet.corvettes[iCount])
            if iCount < len(oEnemyFleet.corvettes):
                for iCount2 in range(0, CORVETTE['num_missiles']):
                    self.missile_queue.append(oEnemyFleet.corvettes[iCount])

        # create a list of user fighters
        lstUserFighters = []
        for carrier in oUserFleet.carriers:
            for fighter in carrier.fighters:
                for iCount2 in range(0, FIGHTER['num_missiles']):
                    lstUserFighters.append(fighter)
        # create a list of enemy fighters
        lstEnemyFighters = []
        for carrier in oEnemyFleet.carriers:
            for fighter in carrier.fighters:
                for iCount2 in range(0, FIGHTER['num_missiles']):
                    lstEnemyFighters.append(fighter)
        # get max fighters between the two
        iMaxFighters = len(lstUserFighters)
        if len(lstUserFighters) < len(lstEnemyFighters):
            iMaxFighters = len(lstEnemyFighters)
        # append each fighter to the queue
        for iCount in range(0, iMaxFighters):
            if iCount < len(lstUserFighters):
                self.missile_queue.append(lstUserFighters[iCount])
            if iCount < len(lstEnemyFighters):
                self.missile_queue.append(lstEnemyFighters[iCount])

    # get a time delay appropriate to the size of the fleets so the battle doesn't end immediately
    def get_delay(self, iCombinedQueueLength):
        # give no delay if the queue is very large
        if iCombinedQueueLength > 200:
            return 0
        iCombinedQueueLength /= 2
        fDelay = round(10 / iCombinedQueueLength, 2)
        return fDelay

# print('User Ships: ' + str(oBattleQueue.user_ships) + '\n')
# print('Enemy Ships: ' + str(oBattleQueue.enemy_ships) + '\n')
# print('Gun Queue: ' + str(oBattleQueue.gun_queue) + '\n')
# print('Missile Queue: ' + str(oBattleQueue.missile_queue) + '\n')

# simulate the battle
def run_battle(oUserFleet, oEnemyFleet, sDifficulty):
    oBattleQueue = BattleQueue(oUserFleet, oEnemyFleet)
    # Before the battle, update the maximum health for each fleet for use in the health meters
    # deprecated
    oBattleQueue.user_fleet.update_max_fleet_health()
    oBattleQueue.enemy_fleet.update_max_fleet_health()

    # loop as long as both fleets have one ship
    while (oBattleQueue.user_ships and oBattleQueue.enemy_ships):
        # run through the gun queue
        # grab the ship from the queue
        oShip = oBattleQueue.gun_queue.pop(0)
        # if the ship is already destroyed, remove the ship and go through the loop again
        while oShip.hit_points <= 0:
            oShip = oBattleQueue.gun_queue.pop(0)

        # handle user ship
        if oShip.fleet.name == USER_FLEET_NAME:
            # get the index of a ship to target
            targetIndex = get_target_index(oBattleQueue.enemy_ships)
            target = oBattleQueue.enemy_ships[targetIndex]
            # if the target fails to dodge calculate damage
            if not target.dodge():
                target.take_damage(oShip.fire_gun())
                # remove the ship from the list if it has been destroyed
                if oBattleQueue.enemy_ships[targetIndex].hit_points == 0:
                    oBattleQueue.enemy_ships.pop(targetIndex)

        # handle enemy ship
        elif oShip.fleet.name == ENEMY_FLEET_NAME:
            # get the index of a ship to target
            targetIndex = get_target_index(oBattleQueue.user_ships)
            target = oBattleQueue.user_ships[targetIndex]
            # if the target fails to dodge calculate damage
            if not target.dodge():
                target.take_damage(oShip.fire_gun())
                # remove the ship from the list if it has been destroyed
                if oBattleQueue.user_ships[targetIndex].hit_points == 0:
                    oBattleQueue.user_ships.pop(targetIndex)
        
        # put the ship at the end of the queue
        oBattleQueue.gun_queue.append(oShip)

        # run through the missile queue
        # first check to see if both ship queues are still populated with at least one ship
        if not (oBattleQueue.user_ships and oBattleQueue.enemy_ships):
            continue
        # grab the ship from the queue
        oShip = oBattleQueue.missile_queue.pop(0)
        # if the ship is already destroyed, remove the ship and go through the loop again
        while oShip.hit_points <= 0:
            oShip = oBattleQueue.missile_queue.pop(0)

        # handle user ship
        if oShip.fleet.name == USER_FLEET_NAME:
            # get the index of a ship to target
            targetIndex = get_target_index(oBattleQueue.enemy_ships)
            target = oBattleQueue.enemy_ships[targetIndex]
            # if the target fails to dodge calculate damage
            if not target.dodge():
                target.take_damage(oShip.fire_missile())
                # remove the ship from the list if it has been destroyed
                if oBattleQueue.enemy_ships[targetIndex].hit_points == 0:
                    oBattleQueue.enemy_ships.pop(targetIndex)

        # handle enemy ship
        elif oShip.fleet.name == ENEMY_FLEET_NAME:
            # get the index of a ship to target
            targetIndex = get_target_index(oBattleQueue.user_ships)
            target = oBattleQueue.user_ships[targetIndex]
            # if the target fails to dodge calculate damage
            if not target.dodge():
                target.take_damage(oShip.fire_missile())
                # remove the ship from the list if it has been destroyed
                if oBattleQueue.user_ships[targetIndex].hit_points == 0:
                    oBattleQueue.user_ships.pop(targetIndex)
        
        # put the ship at the end of the queue
        oBattleQueue.missile_queue.append(oShip)
    
        # print the battle info after each turn
        print(Colors.BOLD + format_title('Battle Info', '~', 10).rjust(TITLE_RIGHT_ADJUST) + Colors.RESET + '\n')
        sOutput = oUserFleet.get_battle_info() + '\n\n'
        sOutput += oEnemyFleet.get_battle_info()
        print(f'{sOutput}')
        # delay slightly if a ship was destroyed
        if oBattleQueue.user_fleet.ship_died or oBattleQueue.enemy_fleet.ship_died:
            time.sleep(0.05)
            oBattleQueue.user_fleet.ship_died = False
            oBattleQueue.enemy_fleet.ship_died = False

        # set a time delay for small battle so they don't end quickly
        # low number of ships should have a longer delay
        time.sleep(oBattleQueue.get_delay(len(oBattleQueue.gun_queue) + len(oBattleQueue.missile_queue)))
        
        # print(CLEAR_CONSOLE)
        os.system('cls')
    
    # print the battle info after the end of the battle
    os.system('cls')
    print(Colors.BOLD + format_title('Battle Info', '~', 10).rjust(TITLE_RIGHT_ADJUST) + Colors.RESET + '\n')
    sOutput = oUserFleet.get_battle_info() + '\n\n'
    sOutput += oEnemyFleet.get_battle_info()
    print(f'{sOutput}')

    oUserFleet.update_fleet()
    oEnemyFleet.update_fleet()

    # print('User Ships: ' + str(oBattleQueue.user_ships) + '\n')
    # print('Enemy Ships: ' + str(oBattleQueue.enemy_ships) + '\n')
    # print('Gun Queue: ' + str(len(oBattleQueue.gun_queue)) + '\n')
    # print('Missile Queue: ' + str(len(oBattleQueue.missile_queue)) + '\n')

    # iCount = 0
    # for ship in oBattleQueue.gun_queue:
    #     if ship.fleet.name == USER_FLEET_NAME:
    #         iCount += 1
    # print('User Ships in Gun Queue: ' + str(iCount))
    # lstShipFleet = []
    # for ship in oBattleQueue.gun_queue:
    #     lstShipFleet.append(ship.fleet.name)
    # print('Gun Queue Fleet: ' + str(lstShipFleet))

def get_target_index(oShips):
    if len(oShips) > 1:
        return random.randrange(0, len(oShips) - 1)
    return 0

# run_battle(oUserFleet, oEnemyFleet)

# oBattleQueue = BattleQueue(oUserFleet, oEnemyFleet)

# print('User Ships: ' + str(oBattleQueue.user_ships) + '\n')
# print('Enemy Ships: ' + str(oBattleQueue.enemy_ships) + '\n')
# print('Gun Queue: ' + str(len(oBattleQueue.gun_queue)) + '\n')
# print('Missile Queue: ' + str(len(oBattleQueue.missile_queue)) + '\n')

# lstShipFleet = []
# for ship in oBattleQueue.gun_queue:
#     lstShipFleet.append(ship.fleet.name)
# print('Gun Queue Fleet: ' + str(lstShipFleet))
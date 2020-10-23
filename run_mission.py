# a separate class to run the mission
from missions import *
from battle import *
from battle_generator import *
from consts import DIFFICULTY
from consts import INVALID_INTEGER
import time
from helper_functions import get_int
import random

class MissionHandler:
    def __init__(self, oUser):
        self.player = oUser
        self.missions = []
        self.generate_missions()

    # generate a set number of missions for the player, with at least one being easy
    def generate_missions(self, iNumMissions=5):
        iFleetValue = self.player.fleets[0].get_fleet_value()
        self.missions.append(Mission('easy', iFleetValue))
        # subtract one mission from the number to add for the easy mission just added
        iNumMissions -= 1

        # create a list of the difficulty keys
        lstKeys = list(DIFFICULTY.keys())

        # randomly create missions until there are no more left to add
        while iNumMissions > 0:
            self.missions.append(Mission(lstKeys[random.randrange(0, len(lstKeys) - 1)], iFleetValue))
            iNumMissions -= 1

    # get a list of missions as a string
    def get_missions(self):
        sOutput = ''
        for iIndex, mission in enumerate(self.missions):
            sOutput += str(iIndex + 1) + ') ' + mission.description.ljust(RIGHT_ADJUST) + '\t' + mission.difficulty.upper() + '\n'
        return sOutput
            
    # handle a mission for a player
    def run_mission(self):
        # show the missions
        print(self.get_missions())

        # select a mission
        iInput = get_int(0, len(self.missions), 'Select a mission, or enter 0 to exit the mission menu: ')

        # handle exiting and invalid input
        if iInput == 0:
            print('Exiting mission menu...\n')
            return
        if iInput == INVALID_INTEGER:
            print('Invalid input\n')
            return
        
        # run the mission
        oMission = self.missions[iInput - 1]
        self.player.mission = oMission

        # ADD FUNCTIONALITY TO SELECT A FLEET LATER

        # print the mission output
        print('')
        print('Starting mission: ' + oMission.description + '...\n')
        print('An enemy fleet has ambushed your convoy!')
        print('Commencing battle...\n')
        time.sleep(3.5)

        # run the battle
        oBattleQueue = BattleQueue(self.player.fleets[0], generate_enemy_fleet(self.player.fleets[0], DIFFICULTY[oMission.difficulty]))
        run_battle(oBattleQueue.user_fleet, oBattleQueue.enemy_fleet, oMission.difficulty)

        # determine the results
        if self.player.fleets[0].get_fleet_health() == 0:
            print('Your fleet was destroyed and its cargo was taken by the enemy!\n')
        else:
            print('Your fleet defeated the enemy fleet.')
            print('Earned ' + Colors.GREEN + str(oMission.value) + Colors.RESET + ' credits.\n')
            oMission.success = True
            self.player.credits += oMission.value

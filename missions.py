# For now, this is a rather barebones class
# In the future it would be nice to add more code to optimize missions
# and create a variety of scenarios, with a value that is determined by statistical methods

# for now a mission will be generated randomly
# the value of the cargo is determined by the 'risk' of the mission
# risky missions that could result in total fleet annilation will bring in very large rewards

import random
import math
# import the difficulty, or risk, of the mission
from consts import DIFFICULTY

# DESTINATIONS
destinations = ('Mars', 'Europa', 'Asteroid Belt')
# TYPES
types = ('Colony', 'Military Base', 'Research Outpost')
# CARGO
cargo = ('food', 'fuel', 'medicine', 'weapons', 'ice')

class Mission:
    LOW_RETURN = 0.05
    MEDIUM_RETURN = 0.20
    HIGH_RETURN = 0.50
    VERY_HIGH_RETURN = 0.75
    IMPOSSIBLE_RETURN = 1.0

    def __init__(self, sDifficulty, iFleetValue):
        self.destination = destinations[random.randrange(0, len(destinations) - 1)]
        self.type = types[random.randrange(0, len(types) - 1)]
        # self.distance
        self.cargo = cargo[random.randrange(0, len(cargo) - 1)]
        self.description = f'{self.destination} {self.type} {self.cargo} delivery'
        self.value = self.get_value(sDifficulty, iFleetValue)
        self.difficulty = sDifficulty
        # set to true if the user completes the mission
        self.success = False

    # # return the string value of the difficulty, capitalized
    # def get_difficulty(self, sDifficulty):
    #     lstDifficulty = list(DIFFICULTY.keys())

    # determine value of mission based on difficulty
    def get_value(self, sDifficulty, iFleetValue):
        fDifficultyRatio = DIFFICULTY[sDifficulty]
        iValue = float(iFleetValue) / 2 * fDifficultyRatio

        if fDifficultyRatio == DIFFICULTY['easy']:
            iValue *= 1 + Mission.LOW_RETURN
        elif fDifficultyRatio == DIFFICULTY['medium']:
            iValue *= 1 + Mission.MEDIUM_RETURN
        elif fDifficultyRatio == DIFFICULTY['hard']:
            iValue *= 1 + Mission.HIGH_RETURN
        elif fDifficultyRatio == DIFFICULTY['very hard']:
            iValue *= 1 + Mission.VERY_HIGH_RETURN
        elif fDifficultyRatio == DIFFICULTY['impossible']:
            iValue *= 1 + Mission.IMPOSSIBLE_RETURN
        
        iValue = int(math.ceil(iValue))

        return iValue
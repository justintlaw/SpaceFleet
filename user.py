# class to define the player
# import necessary files
from ships import *
from consts import *

class User:
    MAX_FLEETS = 5

    def __init__(self):
        self.fleets  = []
        self.credits = 1000000
        self.mission = None

        # create a starting fleet
        self.fleets.append(Fleet(USER_FLEET_NAME))
        for i in range(2):
            self.fleets[0].destroyers.append(create_destroyer(DESTROYER, self.fleets[0]))
        for i in range(4):
            self.fleets[0].corvettes.append(create_corvette(CORVETTE, self.fleets[0]))
        # for i in range(5):
        #     self.fleets.append(create_cargo_ship())
    
    # display a list of info for each fleet with its id
    def get_all_fleet_info(self):
        sOutput = format_title('Fleet Overview', '~', 5) + '\n\n'
        for item in self.fleets:
            sOutput += 'Fleet ID: ' + str(item.id) + '\n' + item.get_info()
        return sOutput + '\n'
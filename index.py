# Program Description
# -A user own's a fleet of ships
# -Cargo ships run missions to get money
# -There is a random chance of being attacked
# -Cargo ships cannot defend themselves
# -if assigned to a fleet with military ships, cargo ships can be defended (this will initiate a battle)

# -GOAL: the user gains money and continues to build a fleet of ships

# import necessary modules
from ships import *
from shop import Shop
from helper_functions import *
from user import User
from colors import Colors
from run_mission import *

# player.fleet[0] = Fleet(USER_FLEET_NAME)

# player.fleet[0].carriers.append(create_carrier(CARRIER, player.fleet[0]))
# player.fleet[0].carriers.append(create_carrier(CARRIER, player.fleet[0]))
# player.fleet[0].carriers.append(create_carrier(CARRIER, player.fleet[0]))
# player.fleet[0].carriers.append(create_carrier(CARRIER, player.fleet[0]))
# player.fleet[0].carriers.append(create_carrier(CARRIER, player.fleet[0]))

# for i in player.fleet[0].carriers:
#     for j in range(10):
#         i.fighters.append(create_fighter(FIGHTER, i, player.fleet[0]))
# for i in range(12):
#     player.fleet[0].destroyers.append(create_destroyer(DESTROYER, player.fleet[0]))
# for i in range (20):
#     player.fleet[0].corvettes.append(create_corvette(CORVETTE, player.fleet[0]))

# variables needed to run program
# Create an instance of the user
player = User()

# TEST
# player.fleets[0].carriers.append(create_carrier(CARRIER, player.fleets[0]))
player.fleets[0].carriers.append(create_carrier(CARRIER, player.fleets[0]))
player.fleets[0].carriers.append(create_carrier(CARRIER, player.fleets[0]))

for i in player.fleets[0].carriers:
    for j in range(10):
        i.fighters.append(create_fighter(FIGHTER, i, player.fleets[0]))
for i in range(5):
    player.fleets[0].destroyers.append(create_destroyer(DESTROYER, player.fleets[0]))
for i in range (10):
    player.fleets[0].corvettes.append(create_corvette(CORVETTE, player.fleets[0]))
# TEST
bKeepPlaying = True

# main menu
print('Welcome to Space Fleet v1.0!\n')
print('Objectives:'.ljust(LEFT_ALIGN) + 'Gain money by running cargo missions to various planets and other locations.')
print(''.ljust(LEFT_ALIGN) + 'Your ships may be attacked while doing missions, so make sure to include both military and civilian vessels in your fleet!\n')

while(bKeepPlaying):
    print(format_title('Main Menu', '-', 3))
    print('1. Manage Fleets')
    print('2. View Missions')
    # add the functionality to save user data to CSV later
    print('3. Save Game')
    print('4. Quit Game\n')
    
    try:
        iUserInput = int(input('Select an option by typing its index: '))
        print('')
    except:
        print('Invalid input.\n')
        continue

    # Manage Fleets
    if iUserInput == 1:
        # print the information for all fleets
        # print(format_title('Fleet Manager', '-', 3) + '\n')
        # print(format_title('Fleet Overview', '~', 5))
        # for item in player.fleets:
        #     print('Fleet ID: ' + str(item.id) + '\n' + item.get_info())
        print(player.get_all_fleet_info())

        # allow the user to repair a fleet, add to a fleet, or take away
        sOutput = f'{Colors.BOLD}Select an option:{Colors.RESET}\t{Colors.CYAN}1. Buy a ship\t'
        sOutput += f'2. Sell a ship\t3. Repair a fleet\t4. Build a fleet\t5. Exit fleet manager{Colors.RESET} '
        # print(sOutput, end='')
        # print('Select an option:')
        # print('1. Repair a fleet')
        # print('2. Buy a ship')
        # print('3. Sell a ship')
        try:
            iUserInput = int(input(sOutput))
            print('')
        except:
            print('Invalid input.\n')
            continue
        
        if iUserInput == 1:
            store = Shop(player)
            store.run_shop(iUserInput)
        elif iUserInput == 2:
            print('Not yet implemented\n')
        elif iUserInput == 3:
            print('Not yet implemented\n')
        elif iUserInput == 4:
            print('Not yet implemented\n')
        elif iUserInput == 5:
            print('Exiting fleet manager\n')
        else:
            print('Enter a valid option.\n')

    # View and perform missions
    elif iUserInput == 2:
        oRunMission = MissionHandler(player)
        oRunMission.run_mission()
    elif iUserInput == 3:
        print('Not yet implemented\n')
    elif iUserInput == 4:
        bKeepPlaying = False
        continue

# def repair_fleet():

# get the index number of a fleet
def get_fleet_index():
    try:
        iUserInput = int(input('Select a fleet index: '))
    except:
        print('Invalid input.\n')
    if (iUserInput >= 0 and iUserInput < len(player.fleets)):
        return iUserInput
    else:
        print('Enter a valid index.')
        get_fleet_index()
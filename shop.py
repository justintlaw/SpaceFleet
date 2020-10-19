# manage repairing a fleet as well as buying and selling ships
from consts import *
from helper_functions import get_int
from colors import Colors
from ships import *
from user import User
LEFT_ADJUST = 15

class Shop:
    def __init__(self, oPlayer):
        self.player = oPlayer

    # method to run the shop
    def run_shop(self, iOption):
        # option 1: buy a ship
        if iOption == 1:
            iFleetIndex = get_int(1, len(self.player.fleets), 'Select a fleet: ')

            # exit shop if there is invalid input
            if (iFleetIndex == INVALID_INTEGER):
                print('Invalid input\n')
                return
                
            # subtract one because the user is selecting the id in the array, not the object
            iFleetIndex -= 1
            
            # display user credits
            print('Amount of credits: ' + Colors.GREEN + format(self.player.credits, 'd') + Colors.RESET + '\n')

            # display ships
            # get strings for each ship, change color to red if can't afford, otherwise green
            sCarrierPrice = Colors.GREEN + str(Carrier.PRICE) + Colors.RESET
            sDestroyerPrice = Colors.GREEN + format(Destroyer.PRICE, 'd') + Colors.RESET
            sCorvettePrice = Colors.GREEN + format(Corvette.PRICE, 'd') + Colors.RESET
            sFighterPrice = Colors.GREEN + format(Fighter.PRICE, 'd') + Colors.RESET

            # booleans to track if a ship can be bought
            bBuyCarrier = True
            bBuyDestroyer = True
            bBuyCorvette = True
            bBuyFighter = True

            # change color FIX LATER
            if Carrier.PRICE > self.player.credits:
                sCarrierPrice = Colors.RED + str(Carrier.PRICE) + Colors.RESET
                bBuyCarrier = False
            if Destroyer.PRICE > self.player.credits:
                sDestroyerPrice = Colors.RED + str(Destroyer.PRICE) + Colors.RESET
                bBuyDestroyer = False
            if Corvette.PRICE > self.player.credits:
                sCorvettePrice = Colors.RED + format(Corvette.PRICE, 'd') + Colors.RESET
                bBuyCorvette = False
            if Fighter.PRICE > self.player.credits:
                sFighterPrice = Colors.RED + format(Fighter.PRICE, 'd') + Colors.RESET
                bBuyFighter = False

            # print shop options
            sShopTitle = format_title('Shop', '~', 3)
            print(sShopTitle)
            print('1. ' + (Carrier.NAME + ':').ljust(LEFT_ADJUST) + sCarrierPrice)
            print('2. ' + (Destroyer.NAME + ':').ljust(LEFT_ADJUST) + sDestroyerPrice)
            print('3. ' + (Corvette.NAME + ':').ljust(LEFT_ADJUST) + sCorvettePrice)
            print('4. ' + (Fighter.NAME + ':').ljust(LEFT_ADJUST) + sFighterPrice)
            print('')

            iInput = get_int(1, 4, 'Enter a ship to purchase: ')

            # exit function if the user enters invalid input
            if (iInput == INVALID_INTEGER):
                print('Invalid input\n')
                return
            
            # make or reject a purchase based on user input
            if iInput == 1:
                if len(self.player.fleets[iFleetIndex].carriers) == Fleet.MAX_CARRIER_SHIPS:
                    print('Maximum amount already reached\n')
                elif bBuyCarrier:
                    self.player.credits -= Carrier.PRICE
                    self.player.fleets[iFleetIndex].carriers.append(create_carrier(CARRIER, self.player.fleets[iFleetIndex]))
                    print('Purchase Successful\n')
                else:
                    print('Not enough credits\n')
            elif iInput == 2:
                if len(self.player.fleets[iFleetIndex].destroyers) == Fleet.MAX_DESTROYER_SHIPS:
                    print('Maximum amount already reached\n')
                elif bBuyDestroyer:
                    self.player.credits -= Destroyer.PRICE
                    self.player.fleets[iFleetIndex].destroyers.append(create_destroyer(DESTROYER, self.player.fleets[iFleetIndex]))
                    print('Purchase Successful\n')
                else:
                    print('Not enough credits\n')
            elif iInput == 3:
                if len(self.player.fleets[iFleetIndex].corvettes) == Fleet.MAX_CORVETTE_SHIPS:
                    print('Maximum amount already reached\n')
                elif bBuyCorvette:
                    self.player.credits -= Corvette.PRICE
                    self.player.fleets[iFleetIndex].corvettes.append(create_corvette(CORVETTE, self.player.fleets[iFleetIndex]))
                    print('Purchase Successful\n')
                else:
                    print('Not enough credits\n')
            elif iInput == 4:
                if len(self.player.fleets[iFleetIndex].carriers) == 0:
                    print('No carriers in fleet for fighters\n')
                elif not self.player.fleets[iFleetIndex].carrier_has_space():
                    print('No carrier has available space\n')
                elif bBuyFighter:
                    # get a list of available carriers
                    lstCarriers = []
                    for carrier in self.player.fleets[iFleetIndex].carriers:
                        if carrier.get_num_fighters() < Carrier.MAX_FIGHTER_SHIPS:
                            lstCarriers.append(carrier)
                    # print the options for the user
                    sOutput = ''
                    for iIndex, carrier in enumerate(lstCarriers):
                        sOutput += str(iIndex + 1) + '. ' + carrier.name + '- '
                        sOutput += 'Fighters: ' + str(carrier.get_num_fighters()) + '/' + str(Carrier.MAX_FIGHTER_SHIPS) + '\n'
                    print(sOutput)
                    # get user input
                    iInput = get_int(1, len(lstCarriers), 'Select a carrier: ')
                    # exit method if input invalid
                    if iInput == INVALID_INTEGER:
                        print('Invalid input\n')
                        return
                    # add the fighter
                    lstCarriers[iInput - 1].fighters.append(create_fighter(Fighter, lstCarriers[iInput - 1], self.player.fleets[iFleetIndex]))
                    self.player.credits -= Fighter.PRICE
                    print('Purchase successful\n')
                else:
                    print('Not enough credits\n')

        # option 2
        
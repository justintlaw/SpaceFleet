from helper_functions import format_title
from helper_functions import progress_bar as health_meter
import random
from consts import *
from colors import Colors

class Fleet:
    MAX_CARGO_SHIPS = 10
    MAX_CARRIER_SHIPS = 5
    MAX_DESTROYER_SHIPS = 20
    MAX_CORVETTE_SHIPS = 50
    next_id = 1

    def __init__(self, sName):
        self.id = Fleet.next_id
        Fleet.next_id += 1
        self.name = sName
        self.num_carrier_ships = 0
        self.num_destroyer_ships = 0
        self.num_corvette_ships = 0
        self.num_fighter_ships = 0
        self.num_cargo_ships = 0
        # use this variable for the health meter
        self.max_fleet_health = 0

        # a fleet is a group of ships
        self.cargo_ships = []
        self.carriers = []
        self.destroyers = []
        self.corvettes = []

        # used to track if a ship has died
        # must be reset to false after its been set to true
        self.ship_died = False
    
    # get the value of the fleet
    def get_fleet_value(self):
        value = 0
        for carrier in self.carriers:
            value += Carrier.PRICE
            for fighter in carrier.fighters:
                value += Fighter.PRICE
        for destroyer in self.carriers:
            value += Destroyer.PRICE
        for corvette in self.corvettes:
            value += Corvette.PRICE
        return value

    # update the fleet to remove any ships that have been destroyed in battle
    def update_fleet(self):
        lstCarriers = []
        lstDestroyers = []
        lstCorvettes = []
        lstFighters = []
    
        for carrier in self.carriers:
            # remove all carrier and all associated fighters if carrier destroyed
            if carrier.hit_points <= 0:
                carrier.fighters.clear()
            # otherwise add carrier back with any destroyed fighters removed
            else:
                # remove all destroyed fighters from carrier, but save ones that are still operating
                for fighter in carrier.fighters:
                    if fighter.hit_points > 0:
                        lstFighters.append(fighter)
                carrier.fighters.clear()
                # add fighters with more than 0 health
                for fighter in lstFighters:
                    carrier.fighters.append(fighter)
                # add carrier back
                lstCarriers.append(carrier)
        
        for destroyer in self.destroyers:
            # remove all destroyers that have been destroyed
            if destroyer.hit_points > 0:
                lstDestroyers.append(destroyer)

        for corvette in self.corvettes:
            # remove all corvettes that have been destroyed
            if corvette.hit_points > 0:
                lstCorvettes.append(corvette)
        
        # clear the fleet to be updated
        self.carriers.clear()
        self.destroyers.clear()
        self.corvettes.clear()

        # reapply the lists to the fleet
        for carrier in lstCarriers:
            self.carriers.append(carrier)
        for destroyer in lstDestroyers:
            self.destroyers.append(destroyer)
        for corvette in lstCorvettes:
            self.corvettes.append(corvette)
        
        # update the counters
        self.num_carrier_ships = len(self.carriers)
        self.num_destroyer_ships = len(self.destroyers)
        self.num_corvette_ships = len(self.corvettes)
        self.num_fighter_ships = 0
        for carrier in self.carriers:
            self.num_fighter_ships += carrier.get_num_fighters()
            
    # display basic information for a fleet
    def get_info(self):
        sOutput = format_title(self.name, '*', 3) + '\n'
        sOutput += 'Fleet Health:'.ljust(LEFT_ALIGN) + '{:.1f}'.format(self.get_fleet_health() / float(self.get_max_fleet_health()) * 100) + '%\t'
        # sOutput += 'Cargo Ships:'.ljust(LEFT_ALIGN) + str(self.num_cargo_ships) + '/' + str(Fleet.MAX_CARGO_SHIPS) + '\t'
        sOutput += 'Carriers:'.ljust(LEFT_ALIGN) + str(self.num_carrier_ships) + '/' + str(Fleet.MAX_CARRIER_SHIPS) + '\t'
        sOutput += 'Destroyers:'.ljust(LEFT_ALIGN) + str(self.num_destroyer_ships) + '/' + str(Fleet.MAX_DESTROYER_SHIPS) + '\t'
        sOutput += 'Corvettes:'.ljust(LEFT_ALIGN) + str(self.num_corvette_ships) + '/' + str(Fleet.MAX_CORVETTE_SHIPS) + '\t'
        sOutput += 'Fighters:'.ljust(LEFT_ALIGN) + str(self.num_fighter_ships) + '/' + str(self.num_carrier_ships * Carrier.MAX_FIGHTER_SHIPS) + '\t'
        return sOutput
    
    # display basic information during battle
    def get_battle_info(self):
        # num_cargo_ships = self.num_cargo_ships
        num_carrier_ships = 0
        num_destroyer_ships = 0
        num_corvette_ships = 0
        num_fighter_ships = 0

        # update the numbers with only ships that are still alive
        for carrier in self.carriers:
            if carrier.hit_points > 0:
                num_carrier_ships += 1
        for destroyer in self.destroyers:
            if destroyer.hit_points > 0:
                num_destroyer_ships += 1
        for corvette in self.corvettes:
            if corvette.hit_points > 0:
                num_corvette_ships += 1
        for carrier in self.carriers:
            for fighter in carrier.fighters:
                if fighter.hit_points > 0:
                    num_fighter_ships += 1

        # temporarily color a ship count red if a ship has been destroyed
        bCarrierDied = False
        bDestroyerDied = False
        bCorvetteDied = False
        bFighterDied = False

        if num_carrier_ships != self.num_carrier_ships:
            bCarrierDied = True
            self.num_carrier_ships = num_carrier_ships
        if num_destroyer_ships != self.num_destroyer_ships:
            bDestroyerDied = True
            self.num_destroyer_ships = num_destroyer_ships
        if num_corvette_ships != self.num_corvette_ships:
            bCorvetteDied = True
            self.num_corvette_ships = num_corvette_ships
        if num_fighter_ships != self.num_fighter_ships:
            bFighterDied = True
            self.num_fighter_ships = num_fighter_ships

        if bCarrierDied or bDestroyerDied or bCorvetteDied or bFighterDied:
            self.ship_died = True

        # don't color red if all ships dead
        if num_carrier_ships == 0 and num_destroyer_ships == 0 and num_corvette_ships == 0 and num_fighter_ships == 0:
            bCarrierDied = False
            bDestroyerDied = False
            bCorvetteDied = False
            bFighterDied = False

        # sOutput = format_title(self.name, '*', 3) + '\n'
        sOutput =  health_meter(self.get_fleet_health(), self.get_max_fleet_health(), prefix=(self.name + ' Health:').ljust(LEFT_ALIGN_METER), length=80, printEnd='\n', fleetName=self.name)
        # sOutput += Colors.CYAN + 'Cargo Ships:'.ljust(LEFT_ALIGN) + str(num_cargo_ships) + '/' + str(Fleet.MAX_CARGO_SHIPS) + '\t'
        sOutput += Colors.CYAN + 'Carriers:'.ljust(LEFT_ALIGN) + Colors.RESET + self.get_ship_num_color(bCarrierDied, num_carrier_ships) + '/' + str(Fleet.MAX_CARRIER_SHIPS) + '\t' + Colors.RESET
        sOutput += Colors.CYAN + 'Destroyers:'.ljust(LEFT_ALIGN) + Colors.RESET + self.get_ship_num_color(bDestroyerDied, num_destroyer_ships) + '/' + str(Fleet.MAX_DESTROYER_SHIPS) + '\t' + Colors.RESET
        sOutput += Colors.CYAN + 'Corvettes:'.ljust(LEFT_ALIGN) + Colors.RESET + self.get_ship_num_color(bCorvetteDied, num_corvette_ships) + '/' + str(Fleet.MAX_CORVETTE_SHIPS) + '\t' + Colors.RESET
        sOutput += Colors.CYAN + 'Fighters:'.ljust(LEFT_ALIGN) + Colors.RESET + self.get_ship_num_color(bFighterDied, num_fighter_ships) + '/' + str(self.num_carrier_ships * Carrier.MAX_FIGHTER_SHIPS) + '\t' + Colors.RESET
        return sOutput
    
    # # get total number of fighters in the fleet
    # def get_total_fighters(self):
    #     iTotal = 0
    #     for item in self.carriers:
    #         iTotal += item.get_num_fighters()

    # helper function for battle info to change the color if a ship was destroyed
    def get_ship_num_color(self, bDied, iShipNum):
        if bDied:
            return Colors.RED + str(iShipNum)
        else:
            return Colors.CYAN + str(iShipNum)
    
    # get the strength of the fleet
    def get_strength(self):
        return self.get_fleet_damage() + self.get_max_fleet_health()
    
    # get the health of an entire fleet
    def get_fleet_health(self):
        iHealth = 0
        # get health in carrier also calculates the health of the fighters
        # CHANGE THIS LATER THIS IS TERRIBLE DONT DO THAT
        for carrier in self.carriers:
            iHealth += carrier.get_health()
        for destroyer in self.destroyers:
            iHealth += destroyer.get_health()
        for corvette in self.corvettes:
            iHealth += corvette.get_health()
        return iHealth
    
    # update the maximum amount of health a fleet may have given the current number of ships
    # deprecated
    def update_max_fleet_health(self):
        iHealth = 0
        for carrier in self.carriers:
            iHealth += CARRIER['hit_points']
            for fighter in carrier.fighters:
                iHealth += FIGHTER['hit_points']
        for destroyer in self.destroyers:
            iHealth += DESTROYER['hit_points']
        for corvette in self.corvettes:
            iHealth += CORVETTE['hit_points']
        self.max_fleet_health = iHealth  
    
    # get the max health of the fleet
    def get_max_fleet_health(self):
        iHealth = 0
        for carrier in self.carriers:
            iHealth += CARRIER['hit_points']
            for fighter in carrier.fighters:
                iHealth += FIGHTER['hit_points']
        for destroyer in self.destroyers:
            iHealth += DESTROYER['hit_points']
        for corvette in self.corvettes:
            iHealth += CORVETTE['hit_points']
        return iHealth  
    
    # get the damage of an entire fleet
    def get_fleet_damage(self):
        iDamage = 0
        for carrier in self.carriers:
            iDamage += carrier.get_damage()
        for destroyer in self.destroyers:
            iDamage += destroyer.get_damage()
        for corvette in self.corvettes:
            iDamage += corvette.get_damage()
        return iDamage

    # determine if there is space for a fighter on any carrier
    def carrier_has_space(self):
        bHasSpace = False
        for carrier in self.carriers:
            if len(carrier.fighters) < Carrier.MAX_FIGHTER_SHIPS:
                bHasSpace = True
                break
        return bHasSpace
    
    # helper function to return the index of a random carrier with an available space for a fighter
    def get_available_carrier_index(self):
        lstIndex = []
        for index, carrier in enumerate(self.carriers):
            if len(carrier.fighters) < Carrier.MAX_FIGHTER_SHIPS:
                lstIndex.append(index)
        return lstIndex[random.randrange(0, len(lstIndex))]
    
    # get max guns for the fleet
    def get_max_guns(self):
        lstGuns = []
        if self.carriers:
            lstGuns.append(CARRIER['num_guns'])
        if self.destroyers:
            lstGuns.append(DESTROYER['num_guns'])
        if self.corvettes:
            lstGuns.append(CORVETTE['num_guns'])
        else:
            return FIGHTER['num_guns']
        
        lstGuns.sort(reverse=True)
        return lstGuns[0]
    
    # get max missiles for the fleet
    def get_max_missiles(self):
        lstMissiles = []
        if self.carriers:
            lstMissiles.append(CARRIER['num_missiles'])
        if self.destroyers:
            lstMissiles.append(DESTROYER['num_missiles'])
        if self.corvettes:
            lstMissiles.append(CORVETTE['num_missiles'])
        else:
            return FIGHTER['num_missiles']
        
        lstMissiles.sort(reverse=True)
        return lstMissiles[0]

class Ship:
    def __init__(self, sName, iSpeed, iHitPoints):
        self.name = sName
        self.speed = iSpeed
        self.hit_points = iHitPoints
    
    def dodge(self):
        return random.random() * 100 < self.speed

# IMPLEMENT CARGO SHIPS LATER
class Cargo:
    def __init__(self, sName, iAmount, iValue):
        self.item_name = sName
        self.item_amount = iAmount
        self.value = iValue

class CargoShip(Ship):
    SMALL_CAPACITY = 100
    MEDIUM_CAPACITY = 500
    LARGE_CAPACITY = 2000

    def __init__(self, sName, iSpeed, iHitPoints, sSize):
        super().__init__(sName, iSpeed, iHitPoints)
        self.size = sSize
        self.cargo_capacity = 0
# IMPLEMENT LATER

class MilitaryShip(Ship):
    GUN_DAMAGE = 20
    MISSILE_DAMAGE = 50

    def __init__(self, sName, iSpeed, iHitPoints, oFleet, iNumGuns, iNumMissiles):
        super().__init__(sName, iSpeed, iHitPoints)
        self.fleet = oFleet
        self.num_guns = iNumGuns
        self.num_missiles = iNumMissiles
        self.shields = 0
    
    def get_damage(self):
        return self.num_guns * MilitaryShip.GUN_DAMAGE + self.num_missiles * MilitaryShip.MISSILE_DAMAGE
    
    def fire_gun(self):
        return MilitaryShip.GUN_DAMAGE
    
    def fire_missile(self):
        return MilitaryShip.MISSILE_DAMAGE

    def take_damage(self, iDamage):
        if self.shields > 0:
            self.shields -= iDamage
            if self.shields < 0:
                self.shields = 0
        else:
            if self.hit_points - iDamage < 0:
                self.hit_points =  0
            else:
                self.hit_points -= iDamage
    
    def get_health(self):
        return self.hit_points

class Carrier(MilitaryShip):
    MAX_FIGHTER_SHIPS = 20
    MAX_SHIELDS = 100
    NAME = 'Carrier'
    PRICE = 100000

    def __init__(self, sName, iSpeed, iHitpoints, oFleet, iNumGuns, iNumMissiles):
        super().__init__(sName, iSpeed, iHitpoints, oFleet, iNumGuns, iNumMissiles)
        self.fleet.num_carrier_ships += 1
        self.fighters = []
        self.shields = 100
    
    def get_num_fighters(self):
        return len(self.fighters)

    # attempts to add a fighter and returns a boolean True if done successfully
    def add_fighter(self, oFighter):
        if self.get_num_fighters() < Carrier.MAX_FIGHTER_SHIPS:
            self.fighters.append(oFighter)
            return True
        else:
            return False

    # get the health of a single carrier, plus its fighters
    def get_health(self):
        iHealth = self.hit_points
        for fighter in self.fighters:
            iHealth += fighter.hit_points
        return iHealth

    # get the damage of a single carrier, plus its fighters
    def get_damage(self):
        iDamage = 0
        iDamage = (self.num_guns * MilitaryShip.GUN_DAMAGE) + (self.num_missiles * MilitaryShip.MISSILE_DAMAGE)
        for fighter in self.fighters:
            iDamage += (fighter.num_guns * MilitaryShip.GUN_DAMAGE) + (fighter.num_missiles * MilitaryShip.MISSILE_DAMAGE)
        return iDamage

class Fighter(MilitaryShip):
    NAME = 'Fighter'
    PRICE = 1500
    def __init__(self, sName, iSpeed, iHitPoints, oFleet, iNumGuns, iNumMissiles, oCarrier):
        super().__init__(sName, iSpeed, iHitPoints, oFleet, iNumGuns, iNumMissiles)
        self.fleet.num_fighter_ships += 1
        self.carrier = oCarrier

class Destroyer(MilitaryShip):
    NAME = 'Destroyer'
    PRICE = 30000
    MAX_SHIELDS = 50

    def __init__(self, sName, iSpeed, iHitPoints, oFleet, iNumGuns, iNumMissiles):
        super().__init__(sName, iSpeed, iHitPoints, oFleet, iNumGuns, iNumMissiles)
        self.fleet.num_destroyer_ships += 1
        self.shields = 50

class Corvette(MilitaryShip):
    NAME = 'Corvette'
    PRICE = 10000
    MAX_SHIELDS = 25

    def __init__(self, sName, iSpeed, iHitPoints, oFleet, iNumGuns, iNumMissiles):
        super().__init__(sName, iSpeed, iHitPoints, oFleet, iNumGuns, iNumMissiles)
        self.fleet.num_corvette_ships += 1
        self.shields = 25

# returns a new carrier based on a dictionary of values
def create_carrier(dictCarrier, oFleet):
    return Carrier(CARRIER['name'], CARRIER['speed'], CARRIER['hit_points'], oFleet, CARRIER['num_guns'], CARRIER['num_missiles'])

# returns a new fighter based on a dictionary of values and a carrier
def create_fighter(dictFighter, oCarrier, oFleet):
    return Fighter(FIGHTER['name'], FIGHTER['speed'], FIGHTER['hit_points'], oFleet, FIGHTER['num_guns'], FIGHTER['num_missiles'], oCarrier)

# returns a new destroyer based on a dictionary of values
def create_destroyer(dictDestroyer, oFleet):
    return Destroyer(DESTROYER['name'], DESTROYER['speed'], DESTROYER['hit_points'], oFleet, DESTROYER['num_guns'], DESTROYER['num_missiles'])

# returns a new corvette based on a dictionary of values
def create_corvette(dictCorvette, oFleet):
    return Corvette(CORVETTE['name'], CORVETTE['speed'], CORVETTE['hit_points'], oFleet, CORVETTE['num_guns'], CORVETTE['num_missiles'])
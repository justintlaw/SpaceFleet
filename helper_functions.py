from colors import Colors
from consts import *

# helper functions
def format_title(sPhrase, sChar, iLength):
    """
    Format a title
    @params:
        sPhrase     -Required : title phrase (Str)
        sChar       -Required : character to surround title (Str)
        iLength     -Required : length of characters on both sides of the title
    """
    sOutput = 'START_KEY#END_KEY'
    sOutput = sOutput.replace('#', sPhrase)
    sOutput = sOutput.replace('START_KEY', sChar * iLength)
    sOutput = sOutput.replace('END_KEY', sChar * iLength)
    return sOutput

# TAKEN AND ADAPTED FROM STACK OVERFLOW
# Print iterations progress
def progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = '', fleetName=''):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    # get the color for the bar
    bar_color = get_health_color(iteration, total)
    # set the prefix color
    prefix_color = ''
    if fleetName == USER_FLEET_NAME:
        prefix_color = Colors.BLUE
    elif fleetName == ENEMY_FLEET_NAME:
        prefix_color = Colors.RED

    sOutput = f'{prefix_color}{prefix}{Colors.RESET}'
    sOutput += f' {bar_color}|{bar}| {percent}% {suffix}{Colors.RESET}' + printEnd
    # Print New Line on Complete
    # if iteration == total: 
    #     print()
    return sOutput

# helper function to get the appropriate color for a health meter
def get_health_color(iteration, total):
    # green if total health is > 75%
    if float(iteration) / float(total) >= 0.75:
        return Colors.GREEN
    # yellow if total health between 0.25 an .75
    elif float(iteration) / float(total) > 0.25:
        return Colors.YELLOW
    # otherwise red
    else:
        return Colors.RED

# make the user enter a valid integer
def get_int(iMin, iMax, sMessage):
    iInput = 0

    iInput = int(input(sMessage))

    if (iInput >= iMin and iInput <= iMax):
        return iInput
    else:
        return -1
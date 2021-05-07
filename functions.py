from clint.textui import colored
from colorama import Fore, Back, Style
from pyfiglet import Figlet
import psutil
import sys
import os

### Colors
def warning(text):
    warning = colored.yellow(text)
    return warning

def success(text):
    success = colored.green(text)
    return success

def inputcolor(text):
    inputcolor = colored.cyan(text)
    return inputcolor


# Função ProcessRunning
def ProcessRunning(ProcessName):
    for proc in psutil.process_iter():
        try:
            if ProcessName in proc.name():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

# Função LoL running
def lolrunning():
    if ProcessRunning("LeagueClient"):
       print(success("[+] ") + "LoL are Running!")
    else:
        print(warning("[!] ") + "LoL are not running!")
        sys.exit() 

########## Change Status  ##########


def checkfileexist():
    file = "status.txt"
    if os.path.exists(file) == False:
        with open(file, mode='a'): pass
        print(warning("[!] ") + file + " not found! Creating the file...")
        sys.exit()

def checkfileempy():
    file = "status.txt"
    if os.stat(file).st_size == 0:
        print(warning("[!] ") + "The file is empty! Canceling... ")
        sys.exit()


########## Menu  ##########

def welcome(text):
    result = Figlet()
    return colored.cyan(result.renderText(text))


def Menu():
    if os.name == 'nt':
         os.system("cls")
    else:
        os.system("clear")
    print(welcome("Spook"))
    print("""
--== Menu ==--
 [1] Icon Changer
 [2] Background Changer
 [3] Rank Changer
 [4] Status Changer
 [5] AutoAccept
 [6] Change Locale
 [7] Offline Status
 [8] Online Status
 [9] More Bots In Practice Tool
 [10] Custom Request
 [0] Exit
--==========--
    """)
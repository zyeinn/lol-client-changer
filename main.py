from lcu_driver import Connector
from functions import *
import time
import sys
import json

# Variable
connector = Connector()

########## Icon Changer Funções  ##########

#Funçao set_icon
async def set_icon(connection):
    id = int(input(inputcolor("[-] ") + "Icon ID: "))
    if id < 78:
        icon = await connection.request('put', '/lol-summoner/v1/current-summoner/icon', data={'profileIconId': id})
        if icon.status == 201:
            print(success("[+] ") + "Success! The Icon ID {0} has been setted!".format(id))
        else:
            print(warning("[!] ") + "Unknown problem, the icon was not set.")
    else:
        icon = await connection.request('put', '/lol-chat/v1/me', data={"icon": id})
        if icon.status == 201:
            print("[+] Success! The Icon ID {0} has been setted!".format(id))
        else:
            print(warning("[!] ") + "Unknown problem, the icon was not set.")


########## Background Changer Funções  ##########
async def set_background(connection):
    id = int(input(inputcolor("[-] ") + "Background ID: "))
    icon = await connection.request('POST', '/lol-summoner/v1/current-summoner/summoner-profile', data={"key": "backgroundSkinId", "value": id})
    if icon.status == 200:
        print(success("[+] ") + "Success! The Background ID {0} has been setted!".format(id))
    else:
        print(warning("[!] ") + "Unknown problem, the icon was not set.")

########## Rank Changer Funções ##########
async def set_rank(connection):
    rank = input(inputcolor("[-] ") + "Rank: ").upper()
    divison = input(inputcolor("[-] ") + "Divison: ").upper()
    response = await connection.request('PUT', '/lol-chat/v1/me', data={ "lol": {"rankedLeagueTier": rank, "rankedLeagueDivision": divison} })
    if response.status == 201:
        print(success("[+] ") + "Success! The rank {0} {1} has been setted!".format(rank, divison))
    else:
        print(warning("[!] ") + "Unknown problem, the rank and division was not set.")

########## Auto Accept ##########

async def autoaccept(connection):
    while True:
        response = await connection.request('GET', '/lol-matchmaking/v1/ready-check')
        status = await response.json()
        print(warning("[!] ") + "Waitting for the Match!")
        if status['state'] == "InProgress":
            send = await connection.request('POST', '/lol-matchmaking/v1/ready-check/accept')
            print(success("[+] ") + "Match Accepted!")
            break
        time.sleep(2)

########## More Bots in Practice Tool ##########
async def morebotspractice(connection):
    with open("practicetool.json", "r") as read_file:
        data = json.load(read_file)
    #print(data)
    response = await connection.request('post', '/lol-lobby/v2/lobby', data=data)
    if response.status == 200:
        print(success("[+] ") + "Success!")
    else:
         print(warning("[!] ") + " Unknown problem, the rank and division was not set.")


########## Change Status  ##########
async def changestatus(connection):
    checkfileexist()
    checkfileempy()
    mystatus = open("status.txt", encoding="utf8").read()
    response = await connection.request('PUT', '/lol-chat/v1/me', data={"statusMessage": mystatus})
    if response.status == 201:
        print(success("[+] ") + "Success! The status has been changed!")
    else:
        print(warning("[!] ") + "Unknown problem, the status was not set.")


######### Change Locate ##########

async def changelocale(connection):
    language = input("[-] Locate: ")
    response = await connection.request('put', '/riotclient/region-locale', data={"locale": language})
    if response.status == 201:
        print(success("[+] ") + "Success! The Client Language to {} has been changed!".format(language))
    else:
        print(warning("[!] ") + "Unknown problem, the Client Language was not set.")

######### User Info ##########
async def getinfo(connection):
    global menuoption
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if summoner.status != 200:
        print(warning("[!] ") + "Login into your account!")
    else:
        resJson = await summoner.json()
        DisplayName = resJson['displayName']
        Level = resJson['summonerLevel']
        print(inputcolor("Username: ") + DisplayName)
        print(inputcolor("Level: ") + Level)
        print("")
        menuoption = int(input(inputcolor("[-] ") + "Enter your choice : "))

########## offlinestatus ##########
async def offinestatus(connection):
    response = await connection.request('put', '/lol-chat/v1/me', data={"availability": "offline"})
    if response.status == 201:
        print(success("[+] ") + "Success! ")
    else:
        print(warning("[!] ") + "Unknown problem, the Offline status was not set.")

########## onlinestatus ##########
async def onlinestatus(connection):
    response = await connection.request('put', '/lol-chat/v1/me', data={"availability": "chat"})
    if response.status == 201:
        print(success("[+] ") + "Success! ")
    else:
        print(warning("[!] ") + "Unknown problem, the Online status was not set.")

##### Custom Request #######
async def customrequest(connection):
    with open("custom.json", "r") as read_file:
        data = json.load(read_file)
    mystatus = open("custom.json", encoding="utf8").read()
    req_endpoint = input("Endpoint: ")
    req_method = input("Request Method: ")
    response = await connection.request(req_method , req_endpoint, data=data)
    print(response)
    print(response.status)

## Ready
lolrunning()
@connector.ready
async def connect(connection):
    Menu()
    await getinfo(connection)
    if menuoption == 1:
        await set_icon(connection)
    elif menuoption == 2:
        await set_background(connection)
    elif menuoption == 3:
        await set_rank(connection)
    elif menuoption == 4:
        await changestatus(connection)
    elif menuoption == 5:
        await autoaccept(connection)
    elif menuoption == 6:
        await changelocale(connection)
    elif menuoption == 7:
        await offinestatus(connection)
    elif menuoption == 8:
        await onlinestatus(connection)
    elif menuoption == 9:
        await morebotspractice(connection)
    elif menuoption == 10:
        await customrequest(connection)
    elif menuoption == 11:
        await teste(connection)
    elif menuoption == 0:
        sys.exit()   
    else:
        print(warning("[!] ") + "Invalid Option")
    
## Close
@connector.close
async def disconnect(connection):
    print(inputcolor("[-] ") + "Exiting...")

connector.start()

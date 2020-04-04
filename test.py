import subprocess
import random

def removeAFK (guestList):  #Creates a list of people online
    players = {}
    for i in list(guestList.keys()):
        if (guestList[i]["playing"] == True):
                players[i] = guestList[i]
    return players

def runGame(players):
    # subprocess.call("cls", shell=True)
    spyIndex = random.choice(list(players.keys()))
    currentPlayers = players
    spy = currentPlayers.pop(spyIndex)
    messagePlayers(spy, currentPlayers)

def messagePlayers (spy, players):
    print (f"{spy['name']}, you are the spy!")
    for i in list(players.keys()):
        print(players[i]["name"] +", you are at this location")

guestList = {0:{"name": "Test", "carrier": "T-Mobile", "playing": False},
    1:{"name": "Hoang Le", "carrier": "Verizon", "playing": True}, 
    2:{"name": "Jon Luu", "carrier": "ATT", "playing": False},
    3:{"name": "Work", "carrier": "Verizon", "playing": True},
    4:{"name": "Jillian Luu", "carrier": "Verizon", "playing": True},
    5:{"name": "Joannaly Tapang", "carrier": "Verizon", "playing": True}}

players = removeAFK(guestList)

flag=True

while flag:
    print(""" 
    **************************************************************************************
    *                                                                                    *
    *        1 - Start New Game                                                          *
    *        2 - End Game                                                                *
    *                                                                                    *
    **************************************************************************************
    """)
    myCommand = input("What would you like to do: ")
    
    print(myCommand)
    if (myCommand == "1"):
        runGame(players)            
    elif (myCommand == "2"):
        flag = False
    else:
        #subprocess.call("cls", shell=True)
        print(f"Your choice of {myCommand} is invalid. Please make a proper selection:")
import subprocess
import random
import SpyfallDB as db
import pandas as pd

def get_player_list():  #Creates a list of people online
    guestList = db.get_all_players()
    players = []
    subprocess.call("cls", shell=True) 
    for element in guestList:
        Flag = True
        while Flag:
            active_player_query = input(f"Is {element['FirstName']} playing?  (Y/N)  ")
            if active_player_query.lower() == "y":
                Flag = False
                element["SpyWeight"] = 100
                element["Location"] = "Location"
                element["SpyCount"] = 0
                players.append(element)
            elif active_player_query.lower() =="n":
                Flag = False
            else:
                print("Please make a valid choice.")         
    return players

def run_game(players):
    #subprocess.call("cls", shell=True)   
    players = set_location(players)
    set_spy(players)
    message_players(players)

def set_location(players):
    # also sets spy weight and increase spy count

    for element in players:
            element["Location"] = "Location"
            element["SpyWeight"] = element["SpyWeight"] + random.randint(1,11)
    return players
    
def set_spy(players):
    my_list = []
    for i in players:
        my_list = my_list + [str(i["UserId"])] * i["SpyWeight"]
    spy_id = int(random.choice(my_list))
    for i in players:
        if i["UserId"] == spy_id:
            i["Location"] = "SPY"
            i["SpyWeight"] = 100
            i["SpyCount"] += 1

def message_players (players):
    for element in players:
        if (element["Location"]) != "SPY":
            print(f"{element['FirstName']}, you are at this location: {element['Location']}")
        else:
            print (f"{element['FirstName']}, you are the spy!")
    print(pd.DataFrame(players))

players = get_player_list()
flag=True
while flag:
    print(""" 
    ************************************
    *                                  *
    *        1 - Start New Game        *
    *        2 - End Game              *
    *                                  *
    ************************************
    """)
    myCommand = input("What would you like to do: ")
    
    print(myCommand)
    if (myCommand == "1"):
        run_game(players)            
    elif (myCommand == "2"):
        flag = False
    else:
        subprocess.call("cls", shell=True)
        print(f"Your choice of {myCommand} is invalid. Please make a proper selection:")
import random
import subprocess


def main():
    guestList = [["Name", "Phone Number", "Carrier", "Playing"],
    ["Hoang Le", "Verizon", True], 
    ["Jon Luu", "ATT", True],
    ["Work", "Verizon", True]]

    locations = ["Locations", "Airplane", "Amusement Park", "Bank", 
    "Beach", "Circus tent", "Corporate Party", "Crusader Army", 
    "Day Spa", "Hotel", "Military Base", "Movie Studio", 
    "Nightclub", "Pirate Ship", "Polar Station", 
    "Police Station", "Restaurant", "Carnival", "Embassy", 
    "Ocean Liner", "School", "University", "Casino", 
    "Hospital", "Passenger Train", "Service Station", 
    "University", "Zoo", "Space Station", "Submarine", 
    "Supermarket", "Theater"]

    location = locations[random.randint(0, len(locations)-1)]

    players = removeAFK(guestList)
    spyIndex = random.randint(0, len(players)-1)
    spy = players[spyIndex]
    players.pop(spyIndex)
    
    subprocess.call("cls", shell=True)
    print (spy[0] + ", you are the spy!" )

    messagePlayers(players, location)
    #print (players)

    
def removeAFK(guestList):
    players = []

    for i in range(len(guestList)):
        if (guestList[i][3] == True):
            players.append(guestList[i])

    return players
    
    
def messagePlayers(players, location):
    for i in range(len(players)):
        print (players[i][0] + ", you are at the " + location +".")


main()

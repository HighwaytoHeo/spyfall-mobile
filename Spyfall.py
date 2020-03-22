def main():
    guestList = [["Name", "Phone Number", "Carrier", False],
    ["Hoang Le", 4082045738, "Verizon", True], 
    ["Work", 5103355199, "Verizon", True]]

    locations = ["Locations", "Airplane", "Amusement Park", "Bank", 
    "Beach", "Circus tent", "Corporate Party", "Crusader Army", 
    "Day Spa", "Hotel", "Military Base", "Movie Studio", 
    "Nightclub", "Pirate Ship", "Polar Sataion", 
    "Police Station", "Restaurant", "Carnival", "Embassy", 
    "Ocean Liner", "School", "University", "Casino", 
    "Hosiptal", "Passenger Train", "Service Station", 
    "Universtiy", "Zoo", "Space Station", "Submarine", 
    "Supermarket", "Theater"]

    removeAFK(guestList)




def removeAFK(guestList):
    players = []

    for i in range(len(guestList)):
        if (guestList[i][3] == True):
            players.append(guestList[i])

    print(players)




main()
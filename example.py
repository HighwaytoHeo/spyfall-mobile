import SpyfallDB
import random
import gmail

class GameSession:
    def __init__(self):
        self._players = {}
        self._num_players = 0
        self.play_again = True
        self.rnd_loc = self.rnd_loc()
        self.timer = 480        # seconds
        
    # using property decorator 
    # a getter function 
    @property
    def players(self): 
        return self._players
    # a setter function 
    @players.setter 
    def players(self, list): 
        for self._id in list:
            self._players[str(self._id)] = Player(self._id)
        for key in self.players:
            self.players[key].is_playing = True
        self._num_players = len(self._players)
            
    # using property decorator 
    # a getter function 
    @property
    def num_players(self): 
        return self._num_players
    
    def rnd_loc(self): 
        self._rnd_loc_df = (SpyfallDB.get_all_locations('df')).sample(n=1)
        self._rnd_loc = self._rnd_loc_df['Location'].values[0]
    
class Player:
    def __init__(self, playerid):
        list = SpyfallDB.get_all_players()
        self._player = [element for element in list if element['PlayerId'] == playerid]
        self._player_id = playerid
        self._fname = [element['FirstName'] for element in self._player][0]
        self._lname = [element['LastName'] for element in self._player][0]
        self._mobile_num = [element['MobileNum'] for element in self._player][0]
        self._mobile_car = [element['MobileCarrier'] for element in self._player][0]
        self._is_spy = False
        self._spy_weight = 100
        self.is_playing = None
    
    # using property decorator 
    # a getter function 
    @property
    def is_spy(self): 
        return self._is_spy
    # a setter function 
    @is_spy.setter 
    def is_spy(self, bval): 
        if bval == True:
            self._is_spy = True
        elif bval == False:
            self._is_spy = False
        else:
            print("Invalid value. Please try again with True or False.")

# Main program
print("Welcome to Spyfall Mobile!\n")
print(SpyfallDB.get_all_players('df'))
ids = [int(x) for x in input("Who's playing?"
                             " (enter PlayerIDs separated by spaces):").split()]

# Create game object instance, players, set to playing
game = GameSession()
game.players = ids

# Hoang's random spy (weighted) algorithm here

# Pick random spy
spy_id = random.choice([*game.players])
game.players[spy_id].is_spy = True
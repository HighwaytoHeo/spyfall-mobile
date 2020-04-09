import configparser
import pymysql
import pandas as pd

class SpyfallDB:
    def __init__(self, conf_file='./spyfalldb.conf'):
        self.config = configparser.ConfigParser()
        self.config.read(conf_file)
        self.host = self.config.get("configuration","hostname")
        self.user = self.config.get("configuration","username")
        self.password = self.config.get("configuration","password")
        self.db = self.config.get("configuration","db_name")
        self.conn = None
        self.cur = None

    def __enter__(self):
        # connect to database
        self.conn = pymysql.connect(host=self.host, 
                                   user=self.user, 
                                   password=self.password, 
                                   db=self.db, cursorclass=pymysql.cursors.DictCursor, 
                                   autocommit=True)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, traceback):
        # params after self are for dealing with exceptions
        self.conn.close()    
        
class SpyfallPlayer:
    def __init__(self, playerid):
        player = [element for element in list if element['PlayerId'] == playerid]
        self.player_id = playerid
        self.fname = [element['FirstName'] for element in player][0]
        self.lname = [element['LastName'] for element in player][0]
        self.mobile_num = [element['MobileNum'] for element in player][0]
        self.mobile_car = [element['MobileCarrier'] for element in player][0]
        self.is_playing = None
        self.is_spy = None
        
    def set_is_playing(self, value):
        if value.lower() == 'true':
            with SpyfallDB() as db:
                query = f"""UPDATE tblGameSession
                        SET IsPlaying = %s
                        WHERE PlayerId = %s"""
                val = (1, self.player_id)
                db.execute(query, val)
            self.is_playing = True
        elif value.lower() == 'false':
            with SpyfallDB() as db:
                query = f"""UPDATE tblGameSession
                        SET IsPlaying = %s
                        WHERE PlayerId = %s"""
                val = (0, self.player_id)
                db.execute(query, val)
            self.is_playing = False
        else:
            return False
        return True
    
    def set_is_spy(self, value):
        if value.lower() == 'true':
            with SpyfallDB() as db:
                query = f"""UPDATE tblGameSession
                        SET IsSpy = %s
                        WHERE PlayerId = %s"""
                val = (1, self.player_id)
                db.execute(query, val)
            self.is_spy = True
        elif value.lower() == 'false':
            with SpyfallDB() as db:
                query = f"""UPDATE tblGameSession
                        SET IsSpy = %s
                        WHERE PlayerId = %s"""
                val = (0, self.player_id)
                db.execute(query, val)
            self.is_spy = False
        else:
            return False
        return True
        
def get_all_players(df=""):
    with SpyfallDB() as db:
        query = 'SELECT * FROM tblPlayer'
        db.execute(query)
        result = db.fetchall()
    if df.lower() == 'df':
        return pd.DataFrame.from_dict(result)   # return dataframe
    else:  
        return result       # return list
    
def get_player(kword, df=""):
    df_temp = get_all_players('df')
    df_lower = df_temp.apply(lambda x: x.astype(str).str.lower())
    # Lambda function to search for the kword anywhere in the dataframe
    row = df_lower.apply(lambda ks: any(ks == str(kword).lower()), axis=1)
    if df.lower() == 'df':
        return df_temp[row]                  # return dataframe
    else:
        return df_temp[row].to_dict('list')  # return dict
    
def add_player(fname, lname, mobilenum, mobilecarrier):
    with SpyfallDB() as db:
        query = """INSERT INTO tblPlayer 
                   (FirstName, LastName, MobileNum, MobileCarrier)
                   VALUES 
                   (%s, %s, %s, %s)"""
        val = (fname, lname, mobilenum, mobilecarrier)
        # Returns number of rows affected
        return db.execute(query, val)
        
def remove_player(playerid):
    with SpyfallDB() as db:
        query = "DELETE FROM tblPlayer WHERE PlayerId = %s"
        # Returns number of rows affected
        return db.execute(query, (playerid))
        
def update_player(attrib, value, playerid):
    df = get_all_players('df')
    # Make column names lower case
    df.columns = map(str.lower, df.columns)
    # Checking that attrib is a valid column name
    if attrib.lower() in df.columns.values.tolist():
        with SpyfallDB() as db:
            query = f"""UPDATE tblPlayer
                    SET {attrib} = %s
                    WHERE PlayerId = %s"""
            val = (value, playerid)
            db.execute(query, val)
    else:
        print("Invalid column name. Please check and try again.")
        return False
    # Test to see if the update was not just successful but also accurate
    upd_row = get_player(value, 'df')
    if (list(upd_row['PlayerId'].values) == [playerid]):
        return 1
    else:
        # print("There is an inconsistency. Double check tblPlayer.")
        return False
    
def get_all_locations(df=""):
    with SpyfallDB() as db:
        query = 'SELECT * FROM tblLocation'
        db.execute(query)
        result = db.fetchall()
    if df.lower() == 'df':
        return pd.DataFrame.from_dict(result)   # return dataframe
    else:  
        return result
    
def get_jobs_by_location(location, df=""):
    locations = get_all_locations('df')
    loc_row = locations[locations['Location'].str.contains(location, case=False)]
    loc_id = int(loc_row['LocationId'].values)
    with SpyfallDB() as db:
        query = f"""SELECT * 
                FROM tblJob
                WHERE LocationId = %s"""
        db.execute(query, loc_id)
        result = db.fetchall()
    if df.lower() == 'df':
        return pd.DataFrame.from_dict(result)   # return dataframe
    else:  
        return result
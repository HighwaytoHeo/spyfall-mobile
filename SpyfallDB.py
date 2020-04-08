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
        
def get_all_players(df=""):
    with SpyfallDB() as db:
        query = 'SELECT * FROM tblUsers'
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
        query = """INSERT INTO tblUsers 
                   (FirstName, LastName, MobileNum, MobileCarrier)
                   VALUES 
                   (%s, %s, %s, %s)"""
        val = (fname, lname, mobilenum, mobilecarrier)
        # Returns number of rows affected
        return db.execute(query, val)
        
def remove_player(userid):
    with SpyfallDB() as db:
        query = "DELETE FROM tblUsers WHERE UserId = %s"
        # Returns number of rows affected
        return db.execute(query, (userid))
        
def update_player(attrib, value, userid):
    df = get_all_players('df')
    # Make column names lower case
    df.columns = map(str.lower, df.columns)
    # Checking that attrib is a valid column name
    if attrib.lower() in df.columns.values.tolist():
        with SpyfallDB() as db:
            query = f"""UPDATE tblUsers
                    SET {attrib} = %s
                    WHERE UserId = %s"""
            val = (value, userid)
            db.execute(query, (val))
    else:
        print("Invalid column name. Please check and try again.")
        return False
    # Test to see if the update was not just successful but also accurate
    upd_row = get_player(value, 'df')
    if (list(upd_row['UserId'].values) == [userid]):
        return upd_row
    else:
        # print("There is an inconsistency. Double check tblUsers.")
        return False
    
def get_all_locations(df=""):
    with SpyfallDB() as db:
        query = 'SELECT * FROM tblLocations'
        db.execute(query)
        result = db.fetchall()
    if df.lower() == 'df':
        return pd.DataFrame.from_dict(result)   # return dataframe
    else:  
        return result
    
def get_jobs_by_location(location, df=""):
    locations = get_all_locations('df')
    loc_row = locations[locations['Location'].str.contains(location)]
    loc_id = int(loc_row['LocationId'].values)
    with SpyfallDB() as db:
        query = f"""SELECT * 
                FROM tblJobs
                WHERE LocationId = %s"""
        db.execute(query, loc_id)
        result = db.fetchall()
    if df.lower() == 'df':
        return pd.DataFrame.from_dict(result)   # return dataframe
    else:  
        return result 
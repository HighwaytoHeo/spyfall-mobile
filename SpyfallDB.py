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
        
def get_all_players(pretty=""):
    with SpyfallDB() as db:
        query = 'SELECT * FROM tblUsers'
        db.execute(query)
        result = db.fetchall()
    if pretty.lower() == 'pretty':
        return pd.DataFrame.from_dict(result)
    else:  
        return result
    
def get_player(kword, pretty=""):
    df = get_all_players('pretty')
    row = df.apply(lambda ks: any(ks == kword), axis=1)
    if pretty.lower() == 'pretty':
        return df[row]
    else:
        return df[row].to_dict('list')
    
def add_player(fname, lname, mobilenum, mobilecarrier):
    with SpyfallDB() as db:
        query = """INSERT INTO tblUsers 
                   (FirstName, LastName, MobileNum, MobileCarrier)
                   VALUES 
                   (%s, %s, %s, %s)"""
        val = (fname, lname, mobilenum, mobilecarrier)
        db.execute(query, val)
        
def del_player(userid):
    empty_row = {'UserId': [], 'FirstName': [], 'LastName': [], 'MobileNum': [], 'MobileCarrier': []}
    with SpyfallDB() as db:
        query = "DELETE FROM tblUsers WHERE UserId = %s"
        db.execute(query, (userid))
    if (get_player(userid) == empty_row):
        return True
    else:
        return False
        
def update_player(attrib, value, userid):
    COL_NAMES = ('FirstName','LastName','MobileNum','MobileCarrier')
    if attrib in COL_NAMES:
        with SpyfallDB() as db:
            query = f"""UPDATE tblUsers
                    SET {attrib} = %s
                    WHERE UserId = %s"""
            val = (value, userid)
            db.execute(query, (val))
    else:
        # print("Invalid column name. Please check and try again.")
        return False
    # Test to see if the update was successful
    upd_row = get_player(userid)
    if (upd_row.get(attrib) == [value]):
        return True
    else:
        # print("There is an inconsistency. Double check tblUsers.")
        return False
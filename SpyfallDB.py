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
        return df[row].to_dict('records')
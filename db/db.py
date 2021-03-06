import sqlite3
import os
from this import d
import pandas as pd

db_dir = os.getenv('SCRAPPER_DB_PATH')
db_path = "{}apartments.db".format(db_dir)

class Database:    
    def __init__(self):
        self.con = sqlite3.connect(db_path)
        self.cursor = self.con.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS apartments
                                (id text PRIMARY KEY,
                                caseId TEXT,
                                company TEXT,
                                longitude TEXT,
                                latitude TEXT,
                                coordinatetype TEXT,
                                street TEXT,
                                house_nr TEXT, 
                                floor TEXT,
                                postcode TEXT,
                                city TEXT,
                                area TEXT,
                                price TEXT,
                                rooms TEXT,
                                daysOnMarket TEXT,
                                type TEXT,
                                descriptiontitle TEXT,
                                descriptionbody TEXT,
                                date TEXT)''')
        self.con.commit()
        if self.con.total_changes==0:
            print("Table created successfully")
        else:  
            print("Table not created")
    
    def insert(self, id, caseId, company, longitude, latitude, coordinate_type, street_name, 
               house_nr, floor, postcode, city, area, price, rooms, daysOnMarket, 
               property_type, description_title, description_body, date):
        self.cursor.execute('''INSERT OR REPLACE 
                               INTO apartments VALUES (
                                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                (id, caseId, company, longitude, latitude, coordinate_type, street_name,
                                house_nr, floor, postcode, city, area, price, rooms, daysOnMarket,
                                property_type, description_title, description_body, date))
        self.con.commit()
    
    def clean_db(self):
        self.cursor.execute("DELETE FROM apartments")
        self.con.commit()
        print("Database cleaned")
    
    def to_string(self):
        for row in self.cursor.execute("SELECT * FROM apartments"):
            print(row)

    def to_csv(self, location):
        conn = sqlite3.connect(db_path, isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
        db_df = pd.read_sql_query("SELECT * FROM apartments", conn)
        db_df.to_csv('{}database.csv'.format(location), index=False)
    
    def get_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM apartments")
        return self.cursor.fetchone()[0]
     
        

#db = Database()
# db.clean_db()
# db.to_string()
# db.insert("test", "test2", 1.0, 2.0, "test1", 1, "test2",  1, 1, 1, 1, "test3", "test4")
# db.insert("test2", "test2", 1.0, 2.0, "test3", 1, "test4", 1, 1, 1, 1, "test5", "test6")
# db.insert("test2", "test2", 1.0, 2.0, "test11", 1, "test4",1, 1, 1, 1, "test5", "test6")
# db.insert("test3", "test2", 1.0, 2.0, "test10", 1, "test4",1, 1, 1, 1, "test5", "test6")

# db.to_string()

#db.to_csv(db_dir)

# print('CSV created')
#df = pd.read_csv('{}database.csv'.format(db_dir))
#print(len(df. index))
# print(df['city'])






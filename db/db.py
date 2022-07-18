import sqlite3
import os
from sqlite3 import dbapi2

class Database:
    def __init__(self):
        db_path = os.getenv('SCRAPPER_DB_PATH')
        path = "{}apartments.db".format(db_path)
        self.con = sqlite3.connect(path)
        self.cursor = self.con.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS apartments
                                (id text PRIMARY KEY,
                                company TEXT,
                                longitude REAL,
                                latitude REAL,
                                address TEXT,
                                postcode INTEGER,
                                city TEXT,
                                area INTEGER,
                                price INTEGER,
                                rooms INTEGER,
                                daysOnMarket INTEGER,
                                type TEXT,
                                link TEXT)''')
        self.con.commit()
        if self.con.total_changes==0:
            print("Table created successfully")
        else:  
            print("Table not created")
    
    def insert(self, id, company, longitude, latitude, address, 
               postcode, city, area, price, rooms, daysOnMarket, 
               type, link):
        self.cursor.execute('''INSERT OR REPLACE 
                               INTO apartments VALUES (
                                '{}','{}','{}','{}','{}',
                                '{}','{}','{}','{}','{}',
                                '{}','{}','{}')'''\
                                .format(id,
                                        company, longitude, latitude, address,
                                        postcode, city, area, price, rooms, daysOnMarket,
                                        type, link))
        self.con.commit()
    
    def readAll(self):
        for row in self.cursor.execute("SELECT * FROM apartments"):
            print(row)

db = Database()
db.insert("test", "test2", 1.0, 2.0, "test1", 1, "test2",  1, 1, 1, 1, "test3", "test4")
db.insert("test2", "test2", 1.0, 2.0, "test3", 1, "test4", 1, 1, 1, 1, "test5", "test6")
db.insert("test2", "test2", 1.0, 2.0, "test11", 1, "test4",1, 1, 1, 1, "test5", "test6")
db.insert("test3", "test2", 1.0, 2.0, "test10", 1, "test4",1, 1, 1, 1, "test5", "test6")
db.readAll()



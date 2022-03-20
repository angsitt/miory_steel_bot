import sqlite3
from datetime import datetime

def add_user_contacts(user_surname, user_name, user_middle_name, user_email):
    try:
        conn = sqlite3.connect('contacts_db')
        c = conn.cursor()

        c.execute('''
                  CREATE TABLE IF NOT EXISTS user_info
                  ([uder_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
                  [user_surname] TEXT,
                  [user_name] TEXT,
                  [user_middle_name] TEXT,
                  [user_email] TEXT,
                  [create_datetime] TEXT)
                  ''')
        conn.commit()

        sql = ("INSERT INTO user_info (user_surname, user_name, user_middle_name, user_email, create_datetime) VALUES (?, ?, ?, ?, ?)")
        c.execute(sql, (user_surname, user_name, user_middle_name, user_email, datetime.now()))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def view_user_contacts():
    conn = sqlite3.connect('contacts_db')
    c = conn.cursor()
    c.execute("SELECT * FROM user_info")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()
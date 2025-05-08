import sqlite3
import pandas as pd

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
def db_setUp():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        organisation TEXT,
        username TEXT,
        passcode TEXT,
        lowerGate INTEGER,
        upperGate INTEGER,
        scheduling_code INTEGER
    )
    """)

    cursor.execute("""
    INSERT INTO users (organisation, username, passcode, lowerGate, upperGate, scheduling_code)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ("carlos & pepes", "carlos", "trial", 62, 68, 412))  # Note: 0412 as int becomes 412

    cursor.execute("""
    INSERT INTO users (organisation, username, passcode, lowerGate, upperGate, scheduling_code)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ("Ubar", "ubar", "tempo", 52, 68, 411))  # 0411 as int becomes 411

    conn.commit()
    conn.close()

    print("Database created and populated with the users table.")



def display_all(): 
    query = "SELECT * FROM users;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    #print(df)

def update_password(username, new_password):
    update_query = "UPDATE users SET passcode = ? WHERE username = ?"
    
    cursor.execute(update_query, (new_password, username))
    
    conn.commit()
    conn.close()
    
    print(f"Password updated for user '{username}' to '{new_password}'.")

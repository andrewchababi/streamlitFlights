import sqlite3
import pandas as pd

def username_password_match(username, password):
    conn = sqlite3.connect('users.db')
    if conn: 
        print("Connection to db worked")
    query = "SELECT passcode FROM users WHERE username = ?"
    df = pd.read_sql_query(query, conn, params=(username,))
    conn.close()
    
    if df.empty:
        return False
    
    stored_passcode = df['passcode'].iloc[0]
    
    return stored_passcode == password

def get_user_info(username):
    conn = sqlite3.connect('users.db')
    if conn: 
        print("Connection: Success")
    query = """
         SELECT organisation, username, lowerGate, upperGate, scheduling_code
        FROM users
        WHERE username = ?
    """
    df = pd.read_sql_query(query, conn, params=(username,))
    conn.close()

    if df.empty:
        return {}
    
    user_dict = df.iloc[0].to_dict()    
    print(user_dict)
    
    return user_dict
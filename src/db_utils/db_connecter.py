import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TON_MDP",  # à adapter
        database="InventaireRPG"
        ssl_disabled=True
    )

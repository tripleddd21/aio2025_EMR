import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nhan2107@",
        database="emr_system"
    )
    return conn
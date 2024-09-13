import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="testdb"
        )
        return connection
    except Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return None

def get_cursor():
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to the database.")
    cursor = connection.cursor()
    return cursor, connection

def close_db_connection(connection):
    if connection:
        connection.close()

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return None

def get_cars_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("CARS_DB_NAME")  
        )
        return connection
    except Error as err:
        print(f"Error connecting to 'cars' database: {err}")
        return None

def get_cursor():
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to the main database.")
    cursor = connection.cursor()
    return cursor, connection

def get_cars_cursor():
    connection = get_cars_db_connection()
    if connection is None:
        raise Exception("Failed to connect to the 'cars' database.")
    cursor = connection.cursor()
    return cursor, connection

def close_db_connection(connection):
    if connection:
        connection.close()

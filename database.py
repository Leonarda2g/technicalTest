
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('mydb.env')

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DATABASE")

#Create Database
def create_database():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    cursor = conn.cursor()
    query = """CREATE DATABASE IF NOT EXISTS """ + MYSQL_DB
    cursor.execute(query)
    conn.close()
    
# Connect to MySQL
def connect():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB   
    )

def initialize_db():
    #Initialize the database with id, name and email
    conn = connect()
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, 
                name VARCHAR(255), 
                email VARCHAR(255),
                phone VARCHAR(255))
    """
    cursor.execute(query)
    conn.close()

#Insert an user into the database with name and email
def create_user(name, email, phone):
    conn = connect()
    cursor = conn.cursor()
    query = """INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)"""
    cursor.execute(query, (name, email, phone))
    conn.commit()
    conn.close()
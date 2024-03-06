import mysql.connector
from mysql.connector import Error
from creds import Creds

def create_connection():
    connection = None
    try: 
        connection = mysql.connector.connect(
            host = Creds.conString,
            user = Creds.userName,
            password = Creds.password,
            database = Creds.dbname
        )
        print('CONNECTED')
    except Error as e:
        print(f"The error '{e}' has occured")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print((f"The error '{e}' has occured"))

def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print((f"The error '{e}' has occured"))
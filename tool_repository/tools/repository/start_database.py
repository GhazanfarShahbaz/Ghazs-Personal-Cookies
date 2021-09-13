import os
import time

import mysql.connector

# activate /env/bin/source

def check_database_status() -> bool:
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="Productivity",
            user="root",
            password="Ghaz5134@",
            auth_plugin='mysql_native_password'
        )
        connection.close()
        return True 
    except:
        return False

def start_myql() -> None:
    os.system("brew services start mysql")
    time.sleep(5)


def stop_myql() -> None:
    os.system("brew services stop mysql")

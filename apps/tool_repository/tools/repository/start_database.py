import time
import mysql.connector

from os import system

# activate /env/bin/source

def check_database_status() -> bool:
    """
    Checks the status of the MySQL database.

    This function connects to the MySQL database and returns True if the connection is successful,
    and False if there is an error.

    Returns:
        A boolean value indicating if the connection was successful (True) or not (False).
    """
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


def start_mysql() -> None:
    """
    Starts the MySQL service.

    This function starts the MySQL service if it is not already running.

    Returns:
        None
    """
    system("brew services start mysql")
    time.sleep(5)


def stop_mysql() -> None:
    """
    Stops the MySQL service.

    This function stops the MySQL service if it is currently running.

    Returns:
        None
    """
    system("brew services stop mysql")

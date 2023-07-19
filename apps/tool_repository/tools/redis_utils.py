"""
file_name = redis_utils.py
Creator: Ghazanfar Shahbaz
Created: 07/18/2023
Last Updated: 07/18/2023
Description: A module representing the EndpointDiagnostics model.
Edit Log:
07/18/2023
-   Created the file
-   Created basic redis client using context manager
"""

from os import getenv
from pickle import load, dump

from redis import Redis, ConnectionPool # pylint: disable=import-error


class RedisClient:
    """
    A class used as a client for the redis databse.
    This creates a connection using a connnection pool and then allows us to execute functions.
    """

    connection_pool: ConnectionPool = ConnectionPool(
        host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), decode_responses=True
    )

    def __init__(self):
        self.connection: Redis = Redis(connection_pool=self.connection_pool)

    def __enter__(self) -> Redis:
        """
        Allows us to setup a context manager with Redis Client.
        More specifically allowing us to use the redis connection that has been 
        created with the connection pool.


        Returns
            A redis connection from teh connection pool.
        """

        return self

    def __exit__(self, type, value, traceback) -> None: #pylint: disable=redefined-builtin
        pass

    def save(self, key: str, value: any, expiration_time=None) -> bool:
        """
        Saves a key to the redis connection.

        Args:
            key: A string representing the key to save.
            value: A strign represting the value associated with the key.
            expiration_time: An optional paramter which can specify when the key will expire.

        Returns:
            A boolean which specifies if the key was successfully saved
        """

        save_value: any = value
        save_type: str = "non_pickle"

        if isinstance(value, dict):
            save_value = dump(value)
            save_type = "pickle"

        self.connection.set(key, save_value)
        # used internally to convert to the correct value type
        self.connection.set(f"__type_{key}__", save_type)

        if expiration_time:
            self.connection.expire(key, expiration_time)
            self.connection.expire(f"__type_{key}__", expiration_time)

        return True

    def get(self, key: str) -> any:
        """
        A method to get the value associated with the given key from redis.

        Args:
            key (str): The key of the value to retrieve.

        Raises:
            KeyError: The given key either did not exist or expired.

        Returns:
            any: The value associated with the given key.
        """

        value: any = self.connection.get(key)

        if value:
            if self.connection.set(f"__type_{key}__") == "pickle":
                value = load(value)
        else:
            raise KeyError("The following key may have expired or does not exist")

        return value


# https://stackoverflow.com/questions/32276493/how-to-store-and-retrieve-a-dictionary-with-redis

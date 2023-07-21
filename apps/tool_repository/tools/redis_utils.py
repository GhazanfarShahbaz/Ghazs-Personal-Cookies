"""
file_name = redis_utils.py
Creator: Ghazanfar Shahbaz
Created: 07/18/2023
Last Updated: 07/19/2023
Description: A module representing the EndpointDiagnostics model.
Edit Log:
07/18/2023
-   Created the file.
-   Created basic redis client using context manager.
07/19/2023
-   Seperated pickle connection from regular redis connection pool.
07/20/2023
-   Added pickle support for list objects
"""

from os import getenv
from pickle import loads, dumps

from redis import Redis, ConnectionPool  # pylint: disable=import-error


class RedisClient:
    """
    A class used as a client for the redis databse.
    This creates a connection using a connnection pool and then allows us to execute functions.
    The first pool is for non pickle objects such as strings.
    The second is for nested dictionary objects.
    """

    # https://stackoverflow.com/questions/32276493/how-to-store-and-retrieve-a-dictionary-with-redis

    connection_pool_native: ConnectionPool = ConnectionPool(
        host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), decode_responses=True
    )

    connection_pool_pickle: ConnectionPool = ConnectionPool(
        host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), decode_responses=False
    )
    # https://github.com/redis/redis-py/issues/809

    def __init__(self):
        self.connection: Redis = Redis(connection_pool=self.connection_pool_native)
        self.pickle_connection: Redis = Redis(
            connection_pool=self.connection_pool_pickle
        )

    def __enter__(self) -> Redis:
        """
        Allows us to setup a context manager with Redis Client.
        More specifically allowing us to use the redis connection that has been
        created with the connection pool.


        Returns
            A redis connection from teh connection pool.
        """

        return self

    def __exit__(  # pylint: disable=redefined-builtin
        self, type, value, traceback
    ) -> None:
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

        if isinstance(value, (dict, list)):
            save_value = dumps(value)
            save_type = "pickle"
            self.pickle_connection.set(key, save_value)

        else:
            self.connection.set(key, save_value)
        # used internally to convert to the correct value type
        self.connection.set(f"__type__{key}__", save_type)

        if expiration_time:
            self.connection.expire(key, expiration_time)
            self.connection.expire(f"__type__{key}__", expiration_time)

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

        value: any = None

        print(key)

        if self.connection.get(f"__type__{key}__") == "pickle":
            value = loads(self.pickle_connection.get(key))
            print("test")
        else:
            value = self.connection.get(key)

        if not value:
            raise KeyError(
                "The following key may have expired, does not exist, or was empty"
            )

        return value

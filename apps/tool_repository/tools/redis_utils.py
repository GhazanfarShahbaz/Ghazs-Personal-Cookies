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

from redis import Redis, ConnectionPool
from os import getenv


class RedisClient:
    connection_pool: ConnectionPool = ConnectionPool(host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), decode_responses=True)

    def __enter__(self) -> Redis:
        """
        Allows us to setup a context manager with Redis Client, more specifically allowing us to use the redis connection that has been created with the connection pool.
        
        
        Returns
            A redis connection from teh connection pool.
        """
        
        connection: Redis = Redis(connection_pool=self.connection_pool)
        return connection
        
    def __exit__(self) -> None:
        pass
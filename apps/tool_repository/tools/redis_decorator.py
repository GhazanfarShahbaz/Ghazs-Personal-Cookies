"""
file_name = redis_decorator.py
Creator: Ghazanfar Shahbaz
Created: 07/20/2023
Last Updated: 07/20/2023
Description: A module used to decorate classes with redis cache.
Edit Log:
07/20/2023
-   Created base decorator
"""

import logging

from apps.tool_repository.tools.redis_utils import RedisClient

logger = logging.getLogger('MainLogger')


class Cache:  # pylint: disable=too-few-public-methods
    """
    A decorator class for caching function results using Redis.


    """

    def __init__(self, cache_key: str, expiration_time=None):
        """
        Initialize an instance of the Cache class.

        Args:
            cache_key (str): The cache key to store/retrieve the cached result.
            expiration_time (int, optional): The expiration time for the cached
            result in seconds. This can be specified as an integer or as a callable
            function that returns an integer. Defaults to None.
        """
        
        self.cache_key = cache_key

        if callable(expiration_time):
            self.expiration_time = expiration_time()
        else:
            self.expiration_time = expiration_time

        logger.info(f"Cache on the following key {self.cache_key} with expiration of {self.expiration_time}")

    def __call__(self, func):
        """
        Callable method to decorate a function with caching logic.

        Args:
            func (callable): The function to be decorated.

        Returns:
            callable: The decorated function.
        """

        def wrapper(*args, **kwargs):
            """
            Wrapper function that handles caching logic for the decorated function.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The result of the decorated function call.
            """

            response: any = None

            with RedisClient() as client:
                try:
                    response = client.get(self.cache_key)
                    logger.info(
                        f"{self.cache_key} exists and is not exired"
                    )
                except KeyError as exception:
                    logger.info(
                        f"The {self.cache_key} key expired or did not exist"
                    )
                    
                    

            if not response:
                response = func(*args, **kwargs)

            with RedisClient() as client:
                client.save(self.cache_key, response, self.expiration_time)

            return response

        return wrapper

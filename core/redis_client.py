from redis.client import Redis
from redis.exceptions import ConnectionError
from django.conf import settings


class RedisClient:
    """ Use dunder method to kill the connection once everything is done. understand how 
        connections are established and maintained."""

    def __init__(self):
        #create redis client and connect using settings
        try:
            self.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=5, socket_timeout=10, retry_on_timeout=True)
            self.pipe = self.redis.pipeline() # created pipeline
        except ConnectionError as e:
            raise ConnectionError("Error occurred while connecting to Redis server")
        except TimeoutError as e:
            raise TimeoutError("Connection to Redis server timed out")
        except Exception as e:
            raise ConnectionError(f"An error occurred while connecting to Redis server: {e}")
    

    def __get_lua_script(self):

        lua_incr_script =   """
                                local current = redis.call('INCR', KEYS[1])
                                if current == 1 then
                                redis.call('EXPIRE', KEYS[1], ARGV[1])
                                end
                                return current
                            """
        
        return lua_incr_script
                



    def update_api_counters(self, key_id): # Assume no null values would be provided for the ratelimiter

        """Note: Understand how multiple requests from various users at the same time will be handled
            cause this would not properly check the allowed number of requests at a prticular time"""
        
        ratelimit_timeperiod =  {
                                    f"minute{key_id}": 60, 
                                    f"hour{key_id}": 60*60,
                                    f"day{key_id}": 24*60*60,
                                    f"month{key_id}": 30*24*60*60, # for 30 days
                                
                                }
        
        # registered_lua_script = self.redis.register_script(self.__get_lua_script)
        loaded_lua_script = self.redis.script_load(self.__get_lua_script()) # load the script and get the sha1 hash of the script to execute it later
        
        for ratelimit_key, expiry in ratelimit_timeperiod.items():
            self.pipe.evalsha(loaded_lua_script, 1, ratelimit_key, expiry) # execute the script for each time period with the respective key and expiry time
        api_key_counters = self.pipe.execute() # execute the pipeline and get the counters for each time period
        api_key_counters = [int(val) if val is not None else 0 for val in api_key_counters ] # convert the counters to integers and handle the case when the key does not exist in redis (i.e. None) by converting it to 0
        return api_key_counters


    def get_api_counters(self, key):
        """for future use check how to
          accept unexpected number of variables if it increases"""

        self.pipe.get(f"minute{key.key_id}")
        self.pipe.get(f"hour{key.key_id}")
        self.pipe.get(f"day{key.key_id}")
        self.pipe.get(f"month{key.key_id}")
        api_key_counters = self.pipe.execute()
        api_key_counters = [int(val) if val is not None else None for val in api_key_counters ]
        return api_key_counters


    def disconnect_redis_server(self):
        try:
            self.redis.close()
        except Exception as e:
            raise ConnectionError(f"An error occurred while disconnecting from Redis server: {e}")
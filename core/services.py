import secrets
import string
from hashlib import sha256

from core.exceptions import KeyGenerationError, KeyValidationError, RateLimitError
from core.redis_client import RedisClient

from datetime import datetime as dt



class KeyGenerator:
    
    # LENGTH_OF_KEY = 50 # this would be set by creater and we dont need it from any user

    def __init__(self, key_length=50): #Default key length 50
        self.__key_length = key_length
        self.__key = None

    def get_keys(self):
        if self.__key_length<32 or self.__key_length>60:
            raise KeyGenerationError(message=f"key length: {self.__key_length} not as per recommended limit")
        self.__key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(self.__key_length))

        hashed_key = self.__get_hashed_key()
        return (self.__key, hashed_key) # returning actual key and hashed key together

    def __get_hashed_key(self):
        try:
            byte_to_hash = self.__key.encode('utf-8')    
            hashed_key = sha256(byte_to_hash).hexdigest() 
        except Exception as e:
            raise KeyGenerationError(message="Error occured during hashing of key")
        else:
            return hashed_key
        


class RateLimitValidator:
    """validates api key and ratelimit for the key, if everything is fine then it updates the count in redis for the key"""


    def __init__(self, key, plan):
        self.key = key
        self.plan = plan

    def __validate_api_key(self):
        """validating the key for different parameters like is it active, is it valid, is the plan active"""
        
        self.__is_key_active()
        self.__is_key_valid()
        self.__is_plan_active()


    def __is_key_active(self):
        if self.key.key_status != 1:
            raise KeyValidationError("Key is not active")
        
    def __is_key_valid(self):
        if self.key.valid_till <= dt.now():
            raise KeyValidationError("key validity expired")
        
    def __is_plan_active(self):
        if self.plan.plan_status !=1:
            raise KeyValidationError("Plan of key not active")
        
    
    def read_API_key(self):
        self.__validate_api_key()
        redis_client = RedisClient()
        api_counters = redis_client.get_api_counters(self.key) # Providing key to read the values.
        self.__check_apikey_threshold(api_counters)
        return self.__write_API_key(redis_client)



    def __check_apikey_threshold(self, api_counters):
        
        timebound_ratelimits =  [
                                    (self.plan.requests_per_minute, "minute"),
                                    (self.plan.requests_per_hour, "hourly"),
                                    (self.plan.requests_per_day, "daily"),
                                    (self.plan.requests_per_month, "monthly"),
                                ]
    
        for index in range(len(api_counters)):
            """checking for the case when the entry exists in the redis, if it does not exist then it will be created with count 1 and ttl, so we dont need to check for that case here"""
            if api_counters[index] is not None and api_counters[index]>=timebound_ratelimits[index][0]:
                raise RateLimitError({"Error":f"{timebound_ratelimits[index][1]} limit exceeded for the key"})


    def __write_API_key(self, redis_client): 
        redis_client.update_api_counters(self.key.key_id) # Redis does not need api key as object only key id is sufficient

        













    

    





        

        


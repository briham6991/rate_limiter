import secrets
import string
from hashlib import sha256
from core.exceptions import KeyGenerationError


class KeyGenerator:
    
    # LENGTH_OF_KEY = 50 # this would be set by creater and we dont need it from any user

    def __init__(self, key_length=50): #Default key length 50
        self.__key_length = key_length
        self.__key = None

    def get_keys(self):
        if self.__key_length<32 or self.__key_length>60:
            raise KeyGenerationError(message=f"key length: {self.__key_length} not as per recommended limit")
        self.__key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(self.__key_length))

        hashed_key = self.get_hashed_key()
        return (self.__key, hashed_key) # returning actual key and hashed key together


    def __get_hashed_key(self):
        try:
            byte_to_hash = self.__key.encode('utf-8')    
            hashed_key = sha256(byte_to_hash).hexdigest() 
        except Exception as e:
            raise KeyGenerationError(message="Error occured during hashing of key")
        else:
            return hashed_key


        

        


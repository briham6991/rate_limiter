
class KeyGenerationError(Exception):

    def __init__(self, message = "Error occured during key generation"):
        self.message = message
        super().__init__(self.message)

        #TODO: see if __str__ helps you to print/log error better

class KeyValidationError(Exception):

    def __init__(self, message = "Invalid Key!"):
        self.message = message
        super().__init__(self.message)


class RateLimitError(Exception):

    def __init__(self, message="Ratelimit exceeded!"):
        self.message = message
        super().__init(self.message)
        
        



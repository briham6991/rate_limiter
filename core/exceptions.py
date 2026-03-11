
class KeyGenerationError(Exception):

    def __init__(self, message = "Error occured during key generation"):
        self.message = message
        super.__init__(self.message)

        #TODO: see if __str__ helps you to print/log error better
        




import unittest
import authentication_app_interaction
import os
import requests

#we import the unittest module to test various units 

class test_token(unittest.TestCase):
    
    def test_auth0_token_obtain(self): # the functions must be all called test_~something~
        print("\ntesting if auth0 token is correctly obtained\n")
        result = authentication_app_interaction.get_token()
        self.assertTrue(result)
        self.assertTrue(result[1] >=200 & result[1] <400)
        
    
    
    def test_request_user_information(self): # the functions must be all called test_~something~
        print("\testing to see if the user information is obtained\n")
        authentication_app_interaction.get_token()
        result = authentication_app_interaction.grab_user_info(os.getenv('example_user_email'),authentication_app_interaction.get_token()[0])
        self.assertTrue(result)
        self.assertTrue(result[1] >=200 & result[1]<400)
        
        
        
        
        




if __name__ == '__main__':
    unittest.main()
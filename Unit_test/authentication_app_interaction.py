
import os
import requests
import json


############################################################################################################################################
############################################################################################################################################
def get_token(): # define function to grab variables 
    auth0_token_request ={ 
        "audience":os.getenv('api_identifier'), # stored relevant details within own system, call variables into a dictionary for HTTP post attempt
        "grant_type":"client_credentials",      #Post attempt done to grab token 
        "client_id":os.getenv('client_id'),
        "client_secret":os.getenv('secret')
        }
    
    post_response = requests.post(os.getenv('auth_token_url'),data = auth0_token_request) #post the auth0_token_request dictionary  and grab reponse code
    grab_info =  requests.post(os.getenv('auth_token_url'),data = auth0_token_request).json() #grab the data sent back including the token code
    token_id = grab_info["access_token"] #use key-value pair to access token
    
    
    #We raise an error here if the desired reponse is not achieved - let the user know of situation if so. 
    if post_response.status_code <200:
        print('Error obtaining value token') # we print instead of raising valuerror for the sake of alexa communication - I.E code keeps running
    elif post_response.status_code >=400:    # and we notify user
        print('Error obtaining value token')
    return token_id,post_response.status_code
    




############################################################################################################################################
############################################################################################################################################
def grab_user_info(email, token_id): # we create a function that takes an email + token in order to grab information from Alfred's backend. 
    http_headers = {"authorization": "Bearer " + token_id}
    url = os.getenv('api_identifier') + "/profile/find-one?email=" + email
    request_user_info = requests.get(url, headers=http_headers)
    post_reponse = request_user_info.status_code
    user_information = request_user_info.json()
    if request_user_info.status_code <200:
        print('Error obtaining value token') # we print instead of raising valuerror for the sake of alexa communication - I.E code keeps running
    elif request_user_info.status_code >=400:    # and we notify user
        print('Error obtaining value token')
    return user_information,post_reponse

############################################################################################################################################
############################################################################################################################################

def send_data_one_off(name_desc,tzid,dates,user_id,token):
    example = {
  "title": name_desc,
  "description": name_desc,
  "timeRuleSet": {
    "tzid": tzid,
    "ruleStrings": [],
    "dates": [dates],
    "excludedDates": [],
    "exclusionRuleStrings": [],
    "until": ""
  },
  "geofenceRuleSet": {},
  "type": "TimeBased",
  "repetitionType": "OneOff",
  "userId": user_id,
  "creator": user_id}
    token_ = token
    headers = {"accept": "application/json",
           "Content-Type": "application/json",
           "Authorization":  "Bearer " + token }
    
    url_ = os.getenv('some_url')
    r = requests.post(url, headers=headers,json=example)





    
    

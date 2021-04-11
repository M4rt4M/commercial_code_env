
import requests
import json
import datetime

def get_token(url,client_id,secret,auth_token_url): # define function to grab variables 
    auth0_token_request ={ 
        "audience":url, # stored relevant details within own system, call variables into a dictionary for HTTP post attempt
        "grant_type":"client_credentials",      #Post attempt done to grab token 
        "client_id":client_id,
        "client_secret":secret
        }
    
    post_response = requests.post(auth_token_url,data = auth0_token_request) #post the auth0_token_request dictionary  and grab reponse code
    grab_info =  requests.post(auth_token_url,data = auth0_token_request).json() #grab the data sent back including the token code
    token_id = grab_info["access_token"] #use key-value pair to access token
    
    
    #We raise an error here if the desired reponse is not achieved - let the user know of situation if so. 
    if post_response.status_code <200:
        print('Error obtaining value token') # we print instead of raising valuerror for the sake of alexa communication - I.E code keeps running
    elif post_response.status_code >=400:    # and we notify user
        print('Error obtaining value token')
    return token_id,post_response.status_code


def grab_email_from_alexa(accesstoken):
    #Fetching user emailaddress from ASK API
    endpoint = "https://api.eu.amazonalexa.com/v2/accounts/~current/settings/Profile.email"
    api_access_token = "Bearer " + accesstoken 
    headers = {"Authorization": api_access_token,
            'Content-Type': 'application/json'}
    r = requests.get(endpoint, headers=headers)
    email = r.json()
    return email

def grab_timezone(accesstoken,device_id):
        #Fetching user emailaddress from ASK API
    device_id_ = device_id
    endpoint = "https://api.eu.amazonalexa.com/v2/devices/{}/settings/System.timeZone".format(device_id_)
    api_access_token = "Bearer " + accesstoken 
    headers = {"Authorization": api_access_token,
                'Content-Type': 'application/json'}
    r = requests.get(endpoint, headers=headers)
    timezone = r.json()
    return timezone



def grab_user_account_id(email, token_id,url_): # we create a function that takes an email + token in order to grab information from Alfred's backend. 
    http_headers = {"authorization": "Bearer " + token_id}
    url = url_ + "/profile/find-one?email=" + email
    request_user_info = requests.get(url, headers=http_headers)
    post_reponse = request_user_info.status_code
    user_information = request_user_info.json()
    if request_user_info.status_code <200:
        print('Error obtaining value token') # we print instead of raising valuerror for the sake of alexa communication - I.E code keeps running
    elif request_user_info.status_code >=400:    # and we notify user
        print('Error obtaining value token')
    return user_information,post_reponse


def post_one_off_prompt(input_,date,time,sub_id,timezone,token,url):
    prompt = {
  "title": input_,
  "description": input_,
  "timeRuleSet": {
    "tzid": timezone,
    "ruleStrings": [],
    "dates": [date + "T" + time +":00.000000"],
    "excludedDates": [],
    "exclusionRuleStrings": [],
    "until": ""},
  "geofenceRuleSet": {},
  "type": "TimeBased",
  "repetitionType": "OneOff",
  "userId": sub_id,
  "creator": sub_id
        
    }
    headers = {"accept": "application/json","Content-Type": "application/json","Authorization":  "Bearer " + token }
    
    r = requests.post(url, headers=headers,json=prompt)
    print(r)
    return r

def convert_tomorrow_format(calendar):
    tomorrow  = str(datetime.date.today() +  datetime.timedelta(days=1))
    if calendar == tomorrow:
        result = "tomorrow"
    else:
        result = calendar
    return result

def find_date_weekday(input_):
    weekdays = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday" : 4,
        "Saturday" :5,
        "Sunday": 6
        }
    date = datetime.date.today()
    while date.weekday() != weekdays[input_]:
        date += datetime.timedelta(1)
    return date


def am_pm_speech(input_):
    first_two_strings = input_[0:2]
    minutes = input_[3:5]
    convert_to_int = int(first_two_strings)
    if convert_to_int <12:
        first_two_strings = str(convert_to_int) + " " +  str(minutes) + " a.m. "
    if convert_to_int >12:
        first_two_strings = str(convert_to_int - 12) + " " + str(minutes) + " p.m. "
    if convert_to_int ==12:
        first_two_strings = str(convert_to_int) + " " +  str(minutes) + " a.m. "
    if convert_to_int ==0:
        first_two_strings = "midnight "
    return first_two_strings

def get_prompts_for_tomrorow(url,token,acc_id):
    trigger_id = [];
    activity = [];
    time = [];
    tomorrow  = str(datetime.date.today() +  datetime.timedelta(days=1))
    url_ = url + "/prompt/in-time-range?start=" + tomorrow + "T00%3A00%3A10.000Z&end=" + tomorrow + "T23%3A59%3A00.000Z"
    headers = {"accept": "application/json", "X-Alfred-User": acc_id,"Authorization":  "Bearer " + token }
    r = requests.get(url_, headers=headers)
    
    for i in range(len(r.json()["triggerTimes"])):
        if (r.json()["triggerTimes"][i]["_id"]) not in trigger_id:
            trigger_id.append(r.json()["triggerTimes"][i]["_id"])
    
    for i in range(len(r.json()["prompts"])):
        for j in range(len(trigger_id)):
            if trigger_id[j] ==r.json()["prompts"][i]["_id"]:
                activity.append(r.json()["prompts"][i]["title"])
                time.append(r.json()["prompts"][i]["timeRuleSet"]["dates"][0][11:16])
            
        
    
    
    return activity,time


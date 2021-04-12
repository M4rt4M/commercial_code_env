
import requests #http requests
import json
import datetime
from datetime import timedelta #timedelta used to add times to date in time format
import os # load environment variables

def get_token(url,client_id,secret,auth_token_url): # define function to grab auth0 token. This function will be used in the Lambda_function.py script. The same applies to all functions below.
    auth0_token_request ={ #create a dictionary that will be sent via post request [key, value]
        "audience":url, # URL_heroku here
        "grant_type":"client_credentials",      
        "client_id":client_id,
        "client_secret":secret
        }
    
    post_response = requests.post(auth_token_url,data = auth0_token_request) #post request with dictioanry
    grab_info =  requests.post(auth_token_url,data = auth0_token_request).json() #convert received data to JSON
    token_id = grab_info["access_token"] #use key in received dictionary to access token
    
    
    #We raise an error here if the desired reponse is not achieved - let the user know of situation if so. 
    if post_response.status_code <200:
        print('Error obtaining value token') # we print instead of raising valuerror for the sake of alexa communication - I.E code keeps running
    elif post_response.status_code >=400:    # and we notify user
        print('Error obtaining value token')
    return token_id,post_response.status_code


def grab_email_from_alexa(accesstoken): #the accesstoken input here will be obtained during the session, it's a simple line of code but permissions must be required --> we notify user to do so
    #Fetching user emailaddress from ASK API
    endpoint = "https://api.eu.amazonalexa.com/v2/accounts/~current/settings/Profile.email"
    api_access_token = "Bearer " + accesstoken 
    headers = {"Authorization": api_access_token, #http header 
            'Content-Type': 'application/json'}
    r = requests.get(endpoint, headers=headers)
    email = r.json()
    return email #return email of user in session

def grab_timezone(accesstoken,device_id): # again the access token and device_id are easily obtained during the session, given the user allows the permission
        #Fetching user emailaddress from ASK API
    device_id_ = device_id
    endpoint = "https://api.eu.amazonalexa.com/v2/devices/{}/settings/System.timeZone".format(device_id_)
    api_access_token = "Bearer " + accesstoken 
    headers = {"Authorization": api_access_token,
                'Content-Type': 'application/json'}
    r = requests.get(endpoint, headers=headers)
    timezone = r.json()
    return timezone # grab timezone of user example: "Europe/London"



def grab_user_account_id(email, token_id,url_): # we create a function that takes an email + token in order to grab information from Alfred's backend. 
    http_headers = {"authorization": "Bearer " + token_id}
    
    url = url_ + "/profile/find-one?email=" + email # after grabbing the email of user in session, we add it to this string in attempts to do a GET request of the profile (assuming email is active on Alfred)
    request_user_info = requests.get(url, headers=http_headers)
    post_reponse = request_user_info.status_code 
    user_information = request_user_info.json()
    if request_user_info.status_code <200:
        print('Error obtaining value token') # we print instead of raising valuerror for the sake of alexa communication - I.E code keeps running
    elif request_user_info.status_code >=400:    # and we notify user
        print('Error obtaining value token')
    return user_information,post_reponse


def post_one_off_prompt(input_,date,time,sub_id,timezone,token,url,tz): # upon grabbing the user details from alfred, we grab the -sub- and use this to send off prompts. 
# the input_ value is the prompt description such as "walk the dog". tz is timezone. the rest of the inputs are self expanatory
    if "Europe/London" in tz: # if the user has a Europe/Londond timezone, we convert to BST time. 
        time_ = (datetime.datetime.strptime(time, '%H:%M')  - timedelta(hours=1)).time()
    elif "Europe/London" not in tz: # if not in Europe/London....for now we keep it UTC time
        time_ = (datetime.datetime.strptime(time, '%H:%M'))
    prompt = { # send this dictionary via a POST request
  "title": input_,
  "description": input_,
  "timeRuleSet": {
    "tzid": timezone,
    "ruleStrings": [],
    "dates": [date + "T" + str(time_) +".000000"],
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
    return r

def convert_tomorrow_format(calendar): # if the user says "tomorrow" we need to somehow grab tomorrow's time, so this function detects if user says string "tomorrow" --> see slot values and alexa interaction 
    tomorrow  = str(datetime.date.today() +  datetime.timedelta(days=1)) # add the date from the current time and add 1 day to get time
    #**we might need to have other considerations for above if the user is in different locations. the date.today may just grab dates according to the lambda host location
    if calendar == tomorrow:
        result = "tomorrow"
    else:
        result = calendar
    return result

def find_date_weekday(input_): # again we create function to convert strings (weekdays) to grab the times 
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
        date += datetime.timedelta(1) #datetime += datetime --> datetime = dateime + datetime
    return date


def am_pm_speech(input_): # alexa's time slots are not speech friendly - alexa will literally say "colon" if one is seen. therefore we add am + pm, and reformulate the dates to alexa says it more user friendly
    first_two_strings = input_[0:2]
    minutes = input_[3:5]
    convert_to_int = int(first_two_strings)
    if minutes == "00": 
        minutes = "" # this is so alexa doesnt say "zero" "zero"
    if convert_to_int <12:
        first_two_strings = str(convert_to_int) + " " +  str(minutes) + " a.m. " # add a.m to speech 
    if convert_to_int >12:
        first_two_strings = str(convert_to_int - 12) + " " + str(minutes) + " p.m. "
    if convert_to_int ==12:
        first_two_strings = str(convert_to_int) + " " +  str(minutes) + " a.m. "
    if convert_to_int ==0:
        first_two_strings = "midnight " # alexa will not say zero zero "24 hour time", instead she says midnight
    return first_two_strings

def get_prompts_for_tomrorow(url,token,acc_id,tz): # function to grab prompts from Alfreds backend
    trigger_id = []; #create empty lists and append  upon finding prompts
    activity = [];
    time = [];
    tomorrow  = str(datetime.date.today() +  datetime.timedelta(days=1)) # get tomorrow's date
    url_ = url + "/prompt/in-time-range?start=" + tomorrow + "T00%3A00%3A10.000Z&end=" + tomorrow + "T23%3A59%3A00.000Z" # add tomorrow's date to url to grab prompts 
    headers = {"accept": "application/json", "X-Alfred-User": acc_id,"Authorization":  "Bearer " + token }
    r = requests.get(url_, headers=headers)
    
    for i in range(len(r.json()["triggerTimes"])): # we grab all the trigger times, go through them and find all the IDs of promtps that are set to be triggered by user
        if (r.json()["triggerTimes"][i]["_id"]) not in trigger_id:
            trigger_id.append(r.json()["triggerTimes"][i]["_id"])
    
    for i in range(len(r.json()["prompts"])): # upon grabbing IDs, we use it to find the title of prompt and time, to tell user 
        for j in range(len(trigger_id)):
            if trigger_id[j] ==r.json()["prompts"][i]["_id"]:
                activity.append(r.json()["prompts"][i]["title"])
                if "Europe/London" in tz:
                    time_ = (datetime.datetime.strptime(r.json()["prompts"][i]["timeRuleSet"]["dates"][0][11:16], '%H:%M')  + timedelta(hours=1)).time()
                elif "Europe/London" not in tz:
                    time_ = (datetime.datetime.strptime(r.json()["prompts"][i]["timeRuleSet"]["dates"][0][11:16], '%H:%M')).time()
                time.append(str(time_))
            
        
    
    
    return activity,time


# -*- coding: utf-8 -*-

# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_model import Response,DialogState
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value
import ask_sdk_core.utils as ask_utils
import os
import requests
import json
import backend


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

###################Note calling weekdays_ = ask_utils.request_util.get_slot(handler_input, "weekdays")
#####when there is no slot in the intent will return None
######Note calling speak_output = "{}".format(handler_input.attributes_manager.session_attributes["weekdays"]) where the session variable was assigned to --> ask_utils.request_util.get_slot(handler_input, "weekdays")


class LaunchRequestHandler(AbstractRequestHandler):

    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #These variablles must be declared below, otherwise calling them will cause an exception error. calling non-existent slot values incontrast prvoides a NULL value
        #handler_input.attributes_manager.session_attributes["First_time"] = False # declare session variable to let intents know whether to guide user or not for future speeches
        handler_input.attributes_manager.session_attributes["user_confirmed_input"] = False # did the user fill in the input slot
        handler_input.attributes_manager.session_attributes["user_confirmed_weekday_time"] = False # did the user fill in the weekday slot
        handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] = False # did the user fill in the time and date slots
        
        
        return ask_utils.is_request_type("LaunchRequest")(handler_input)
        
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = '<speak> \
                        <voice name="Matthew"> \
						<amazon:domain name="conversational"> \
                        Hello! My name is Alfred, and I am here to help you remember things better. I can set, and give you reminders. Would you like to set a reminder now? \
                        </amazon:domain> \
						</voice> \
                        </speak>' 
        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
        reprompt = '<speak> \
                    <voice name="Matthew"> \
					<amazon:domain name="conversational"> \
					If you need further guidance, you can say: help, or: I need assistance. \
                    </amazon:domain> \
					</voice> \
                    </speak>'
        return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)

#note calling a session attribute that wasnt initially declared, classifies the value as NULL or None --> very useful. 
class setreminderdescriptionIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        handler_input.attributes_manager.session_attributes["user_confirmed_input"] = True
        return ask_utils.is_intent_name("setremindertype")(handler_input)
    def handle(self, handler_input):
        #note calling a sllot value using ask_utils.request_util.get_slot(handler_input,~~) that wasnt initially declared classifies the value as NULL or None --> Potentially very useful for variable checks.
        
        input_ = ask_utils.request_util.get_slot(handler_input, "input")
        handler_input.attributes_manager.session_attributes["input"] =input_.value
        novalues_ = ask_utils.request_util.get_slot(handler_input, "novalues")
        
        
        try:
            if handler_input.attributes_manager.session_attributes["First_time"] == True and input_.value != None:
                # This will be triggerred the first time user makes a prompt, after they provided the prompt label when initialising the skill 
                speak_output = '<speak> \
                                <voice name="Matthew"> \
						        <amazon:domain name="conversational"> \
						        Now that you have set a reminder to: {}, you can set the date and time. As an example, you can say: remind me at seven a.m, next Monday. \
						        </amazon:domain> \
						        </voice> \
                                </speak>'.format(input_.value)
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
            else:
                speak_output = "{}".format(handler_input.attributes_manager.session_attributes["First_time"])
        except:
            speak_output = "Thanks, What date and time would you like for your reminder?"
            handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
        
        try:
            if input_.value != None and handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] == True:
                try:
                    if handler_input.attributes_manager.session_attributes["time"] != None and handler_input.attributes_manager.session_attributes["date"] != None:
                        speak_output = '<speak> \
                                        <voice name="Matthew"> \
						                <amazon:domain name="conversational"> \
						                You have set a reminder to: {}. for {}, at {}. Is that correct?\
						                </amazon:domain> \
						                </voice> \
                                        </speak>'.format(input_.value,handler_input.attributes_manager.session_attributes["date"],backend.am_pm_speech(handler_input.attributes_manager.session_attributes["time"]))
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["date_time_input_ready"] = True
                        if backend.convert_tomorrow_format(handler_input.attributes_manager.session_attributes["date"])=="tomorrow":
                            speak_output ="You have set a reminder to: {}. at {},{}. Is that correct?".format(handler_input.attributes_manager.session_attributes["input"],backend.am_pm_speech(handler_input.attributes_manager.session_attributes["time"]),"tomorrow")
                except:
                    pass
                
                try:
                    if handler_input.attributes_manager.session_attributes["time"] != None and handler_input.attributes_manager.session_attributes["weekdays"] != None:
                        speak_output = "You have set a reminder to: {}. for next {}, at {}. Is that correct?".format(input_.value,handler_input.attributes_manager.session_attributes["weekdays"],backend.am_pm_speech(handler_input.attributes_manager.session_attributes["time"]))
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["date_time_input_ready"] = True
                except:
                    pass
        except:
            pass


        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["date_only_provided"] != None:
                handler_input.attributes_manager.session_attributes["date_time_input_ready"] = True
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                input_.value,handler_input.attributes_manager.session_attributes["date"] = input_.value,handler_input.attributes_manager.session_attributes["date_only_provided"]
                input_.value,handler_input.attributes_manager.session_attributes["time"] = input_.value,handler_input.attributes_manager.session_attributes["time_only_provided"]
                speak_output = "You have set a reminder to: {}. for {}, at {}. Is that correct?".format(input_.value,handler_input.attributes_manager.session_attributes["date_only_provided"],backend.am_pm_speech(handler_input.attributes_manager.session_attributes["time_only_provided"]))
                if backend.convert_tomorrow_format(handler_input.attributes_manager.session_attributes["date"])=="tomorrow":
                    speak_output ="You have set a reminder to: {}. at {},{}. Is that correct?".format(handler_input.attributes_manager.session_attributes["input"],backend.am_pm_speech(handler_input.attributes_manager.session_attributes["time"]),"tomorrow")
        except:
            pass
        
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["weekday_only_provided"] != None:
                speak_output = "you have set a reminder to {}. for next {}, at {}. Is that correct?".format(input_.value,handler_input.attributes_manager.session_attributes["weekday_only_provided"],backend.am_pm_speech(handler_input.attributes_manager.session_attributes["time_only_provided"]))
                handler_input.attributes_manager.session_attributes["date_time_input_ready"] = True
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                input_.value,handler_input.attributes_manager.session_attributes["weekdays"] = input_.value,handler_input.attributes_manager.session_attributes["weekday_only_provided"]
                input_.value,handler_input.attributes_manager.session_attributes["time"] = input_.value,handler_input.attributes_manager.session_attributes["time_only_provided"]
        except:
            pass
        
        if novalues_.value != None:
            speak_output = "What would you like me to remind you about?"
            try:
                if handler_input.attributes_manager.session_attributes["First_time"] == True:
                    speak_output = "What would you like me to remind you about? For example, you can say: remind me to walk the dog"
            except:
                pass
        try:
            handler_input.attributes_manager.session_attributes["accesstoken"] = str(handler_input.request_envelope.context.system.api_access_token) # grab id token of current user 
            handler_input.attributes_manager.session_attributes["email_grab_alexa"] = backend.grab_email_from_alexa(handler_input.attributes_manager.session_attributes["accesstoken"])#grabbed the email of the current user.
            handler_input.attributes_manager.session_attributes["device_id"] = str(handler_input.request_envelope.context.system.device.device_id) # grab timezone of current user
        except:
            speak_output = "I'm sorry, but this skill does not have permission to accept certain information. Please change this through your skill settings."
        
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)


class datetimeIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("setdatetimeintent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #note calling the things below that wasnt initially declared, classifies the value as NULL or None --> very useful.
        date_ =ask_utils.request_util.get_slot(handler_input, "date")
        time_ =ask_utils.request_util.get_slot(handler_input, "time")
        weekdays_ = ask_utils.request_util.get_slot(handler_input, "weekdays")
        input_ = ask_utils.request_util.get_slot(handler_input, "input")
        speak_output="test 1 2 3 4"
        
        
        try:
            if weekdays_.value != None and time_.value != None:
                speak_output = "Thank you! Now, what would you like me to remind you about?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["time"] = time_.value
                handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] = True
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "Thank you, now that you have set the date and time, you can tell me what to remind you about. For example you can say: remind me to take my medication."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["time"] = time_.value
                        handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] = True
                except:
                    pass
        except:
            pass
        
        try:
            if date_.value != None and time_.value != None and handler_input.attributes_manager.session_attributes["user_confirmed_input"] == True:
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["date"] = date_.value
                handler_input.attributes_manager.session_attributes["time"] = time_.value
                handler_input.attributes_manager.session_attributes["date_time_input_ready"] = True
                speak_output ="You have set a reminder to {}. at {},{}. Is that correct?".format(handler_input.attributes_manager.session_attributes["input"],backend.am_pm_speech(time_.value),date_.value)
                if backend.convert_tomorrow_format(handler_input.attributes_manager.session_attributes["date"])=="tomorrow":
                    speak_output = '<speak> \
                                    <voice name="Matthew"> \
						            <amazon:domain name="conversational"> \
						            You have set a reminder to {}. at {},{}. Is that correct? \
						            </amazon:domain> \
						            </voice> \
                                    </speak>'.format(handler_input.attributes_manager.session_attributes["input"],backend.am_pm_speech(time_.value),"tomorrow")
            elif weekdays_.value != None and time_.value != None and  handler_input.attributes_manager.session_attributes["user_confirmed_input"] == True:
                speak_output ="You have set a reminder to {}, for next {}, at {}. Is that correct?".format(handler_input.attributes_manager.session_attributes["input"],weekdays_.value,backend.am_pm_speech(time_.value))
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["weekdays"] = weekdays_.value
                handler_input.attributes_manager.session_attributes["time"] = time_.value#
                handler_input.attributes_manager.session_attributes["date_time_input_ready"] = True
                handler_input.attributes_manager.session_attributes["date"] = backend.find_date_weekday(handler_input.attributes_manager.session_attributes["weekdays"])#
                
            elif date_.value != None and time_.value != None:
                speak_output = "Thank you! Now, what would you like me to remind you about?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] = True
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "Thank you. Now that you have set the date and time, please tell me what to remind you about. As an example you can say: remind me to prepare lunch."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
                handler_input.attributes_manager.session_attributes["date"] = date_.value#
                handler_input.attributes_manager.session_attributes["time"] = time_.value#
                handler_input.attributes_manager.session_attributes["weekdays"] = weekdays_.value# this value will be set to NULL/None
                try:
                    
                    if handler_input.attributes_manager.session_attributes["weekdays"] != None:
                        handler_input.attributes_manager.session_attributes["date"] = backend.find_date_weekday(handler_input.attributes_manager.session_attributes["weekdays"])
                except:
                    pass
                    
        
        except:
            if handler_input.attributes_manager.session_attributes["input"] == None:
                handler_input.attributes_manager.session_attributes["weekdays"] = weekdays_.value
                speak_output = "Thank you. Now, what would you like me to remind you about?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["user_confirmed_weekday_time"] = True
            #elif handler_input.attributes_manager.session_attributes["date"] == None:
            #    speak_output = "What date would you like for your reminder?"
            #    handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                
            try:
                if handler_input.attributes_manager.session_attributes["First_time"] == True:
                    speak_output = "Thank you. Now that you have set the date and time, please tell me what to remind you about. For example you can say: remind me to take my medication."
                    handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
            except:
                pass
            handler_input.attributes_manager.session_attributes["date"] = date_.value
            handler_input.attributes_manager.session_attributes["time"] = time_.value
            handler_input.attributes_manager.session_attributes["weekdays"] = weekdays_.value
            
            try:
                    
                if handler_input.attributes_manager.session_attributes["weekdays"] != None:
                    handler_input.attributes_manager.session_attributes["date"] = backend.find_date_weekday(handler_input.attributes_manager.session_attributes["weekdays"])
            except:
                pass
                
            
            
        try:
            if handler_input.attributes_manager.session_attributes["date_only_provided"] != None and time_.value != None:
                speak_output = "Thank you. Now, what would you like me to remind you about?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["time"] = time_.value
                handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] = True
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "Thank you. Now that you have set the date and time, please tell me what to remind you about. For example you can say: remind me to take my medication."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["time"] = time_.value
                except:
                    pass
                        
        except:
            pass
        
        try:
            if date_.value != None and time_.value == None:
                speak_output = "Thanks. Now, what time would you like to set for this reminder?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["date_only_provided"] = date_.value
                handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] = True
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output ="That's great. Now that you have set the date, please tell me what time to remind you. For example, you can say: seven a.m."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
        except:
            pass
        
        try:
            if weekdays_.value != None and time_.value ==None:
                speak_output = "Thanks. Now, what time would you like to set for this reminder?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["weekday_only_provided"] = weekdays_.value
                handler_input.attributes_manager.session_attributes["user_confirmed_weekday_time"] = True
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output ="That's great. Now that you have set the date, please tell me what time to remind you. For example, you can say: seven a.m."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["weekday_only_provided"] = weekdays_.value
                except:
                    pass
        except:
            pass

        try:
            if time_.value != None and weekdays_.value == None and date_.value == None:
                speak_output = "Thanks. Now, what date would you like to set for this reminder?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["time_only_provided"] = time_.value
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output ="That's great. Now that you have set the time, please tell me what date would you like to set for this reminder For example, you can say: tomorrow, or: next Monday."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
        except:
            pass
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["weekday_only_provided"] != None:
                speak_output = "That's great. Now, what would you like me to remind you about?"
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "that's great. Now, what would you like me to remind you about? For example, you can say: remind me to buy bread."
                except:
                    pass
        except:
            pass
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["date_only_provided"] != None:
                speak_output = "That's great. Now, what would you like me to remind you about?"
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "that's great. Now, what would you like me to remind you about? For example, you can say: remind me to buy bread."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
        except:
            pass
        
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["date_only_provided"] != None and handler_input.attributes_manager.session_attributes["input"] != None:
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["date_time_input_ready"] = True
                handler_input.attributes_manager.session_attributes["date"] = handler_input.attributes_manager.session_attributes["date_only_provided"]
                handler_input.attributes_manager.session_attributes["time"] = handler_input.attributes_manager.session_attributes["time_only_provided"]
                speak_output = "You have set a reminder to {}. for {}, at {}. Is that correct? ".format(handler_input.attributes_manager.session_attributes["input"],handler_input.attributes_manager.session_attributes["date_only_provided"],backend.am_pm_speech(handler_input.attributes_manager.session_attributes["time_only_provided"]))
                if backend.convert_tomorrow_format(handler_input.attributes_manager.session_attributes["date"]) =="tomorrow":
                    speak_output ="You have set a reminder to: {}. at {},{}. Is that correct?".format(handler_input.attributes_manager.session_attributes["input"],backend.am_pm_speech(time_.value),"tomorrow")
        except:
            pass
        
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["weekday_only_provided"] != None and handler_input.attributes_manager.session_attributes["input"] != None:
                
                speak_output = "You have set a reminder to {}. for next {}, at {}. Is that correct? ".format(handler_input.attributes_manager.session_attributes["input"],handler_input.attributes_manager.session_attributes["weekday_only_provided"],backend.am_pm_speech(handler_input.attributes_manager.session_attributes["time_only_provided"]))
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["date_time_input_ready"] = True
                handler_input.attributes_manager.session_attributes["time"] = handler_input.attributes_manager.session_attributes["time_only_provided"]
                handler_input.attributes_manager.session_attributes["weekdays"] = handler_input.attributes_manager.session_attributes["weekday_only_provided"]
                handler_input.attributes_manager.session_attributes["date"] = backend.find_date_weekday(handler_input.attributes_manager.session_attributes["weekdays"])#
        except:
            pass
        
        try:
            handler_input.attributes_manager.session_attributes["accesstoken"] = str(handler_input.request_envelope.context.system.api_access_token) # grab id token of current user 
            handler_input.attributes_manager.session_attributes["email_grab_alexa"] = backend.grab_email_from_alexa(handler_input.attributes_manager.session_attributes["accesstoken"])#grabbed the email of the current user.
            handler_input.attributes_manager.session_attributes["device_id"] = str(handler_input.request_envelope.context.system.device.device_id) # grab timezone of current user
        except:
            speak_output = "I'm sorry, but this skill does not have permission to accept certain information. Please change this through your skill settings."
                        
                
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)



class yesIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "What reminder would you like?"
        listen_or_end = handler_input.response_builder.speak(speak_output).ask(speak_output).response
        try:
            if handler_input.attributes_manager.session_attributes["input"] != None:
                speak_output = "I'm sorry, I don't know what you're saying yes to"
        except:
            pass
        try:
            if handler_input.attributes_manager.session_attributes["date_time_input_ready"] == True:
                #####################################################################################################
                #####################################################################################################
                try:
                    handler_input.attributes_manager.session_attributes["secret"] = os.getenv('secret')
                    handler_input.attributes_manager.session_attributes["auth_url"] = os.getenv('auth_url')
                    handler_input.attributes_manager.session_attributes["client_id"] = os.getenv('client_id')
                    handler_input.attributes_manager.session_attributes["url_heroku"] = os.getenv('url_heroku')
                    handler_input.attributes_manager.session_attributes["url_post"] = os.getenv('url_post')
                    accesstoken = str(handler_input.request_envelope.context.system.api_access_token) # grab id token of current user 
                    email_grab_alexa = backend.grab_email_from_alexa(accesstoken)#grabbed the email of the current user.
                    device_id = str(handler_input.request_envelope.context.system.device.device_id) # grab timezone of current user
                    auth_token_grab = backend.get_token(handler_input.attributes_manager.session_attributes["url_heroku"],handler_input.attributes_manager.session_attributes["client_id"],handler_input.attributes_manager.session_attributes["secret"],handler_input.attributes_manager.session_attributes["auth_url"])
                    token = auth_token_grab[0] # grabbed the token for auth0 
                    grab_timezone = backend.grab_timezone(handler_input.attributes_manager.session_attributes["accesstoken"],handler_input.attributes_manager.session_attributes["device_id"])##grab timezone of current user
                    
                    grab_alfred_id = backend.grab_user_account_id(email_grab_alexa.lower(),token,handler_input.attributes_manager.session_attributes["url_heroku"]) #Grab ID of current user  N.B - email needs to be all lower case. 
                    
                    post_test = backend.post_one_off_prompt(handler_input.attributes_manager.session_attributes["input"],handler_input.attributes_manager.session_attributes["date"],handler_input.attributes_manager.session_attributes["time"],grab_alfred_id[0]["sub"],grab_timezone,token,handler_input.attributes_manager.session_attributes["url_post"])
                    
                    speak_output = "That's great. Your prompt now has been set."
                    handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                    listen_or_end = handler_input.response_builder.speak(speak_output).response
                    try:
                        if handler_input.attributes_manager.session_attributes["First_time"] == True:
                            speak_output ="That's great. Your prompt has been set. Next time, you can start setting a prompt by saying: Alexa, tell Alfred, remind me to {}".format(handler_input.attributes_manager.session_attributes["input"])
                            listen_or_end = handler_input.response_builder.speak(speak_output).response
                    except:
                        pass
                except:
                    speak_output = "Apologies, we had trouble connecting this skill to Alfred"
                    listen_or_end = handler_input.response_builder.speak(speak_output).response
        except:
            pass

        return listen_or_end

class NoIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        
        speak_output ="Apologies. I don't understand what you're saying no to."
        end_session_or_not = handler_input.response_builder.speak(speak_output).ask(speak_output).response
        try:
            if handler_input.attributes_manager.session_attributes["date_time_input_ready"] == True:
                speak_output = "No worries. You can try again anytime. Bye now!"
                end_session_or_not = handler_input.response_builder.speak(speak_output).response
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "No worries. You can re-initialise the skill by saying: Alexa, tell Alfred remind me to: followed by your prompt. See you soon!"
                        end_session_or_not = handler_input.response_builder.speak(speak_output).response
                except:
                    pass
        except:
            pass
        return end_session_or_not

class whatpromptsIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("whatpromptstomorrow")(handler_input)

    def handle(self, handler_input):
        speak_output = ""
        try:
        handler_input.attributes_manager.session_attributes["secret"] = os.getenv('secret')
        handler_input.attributes_manager.session_attributes["auth_url"] = os.getenv('auth_url')
        handler_input.attributes_manager.session_attributes["client_id"] = os.getenv('client_id')
        handler_input.attributes_manager.session_attributes["url_heroku"] = os.getenv('url_heroku')
        handler_input.attributes_manager.session_attributes["url_post"] = os.getenv('url_post')
            auth_token_grab = backend.get_token(handler_input.attributes_manager.session_attributes["url_heroku"],handler_input.attributes_manager.session_attributes["client_id"],handler_input.attributes_manager.session_attributes["secret"],handler_input.attributes_manager.session_attributes["auth_url"])
            token = auth_token_grab[0] # grabbed the token for auth0
            handler_input.attributes_manager.session_attributes["accesstoken"] = str(handler_input.request_envelope.context.system.api_access_token) # grab id token of current user 
            handler_input.attributes_manager.session_attributes["email_grab_alexa"] = backend.grab_email_from_alexa(handler_input.attributes_manager.session_attributes["accesstoken"])#grabbed the email of the current user.
            email_grab_alexa = handler_input.attributes_manager.session_attributes["email_grab_alexa"]          
            grab_alfred_id = backend.grab_user_account_id(email_grab_alexa.lower(),token,handler_input.attributes_manager.session_attributes["url_heroku"])[0]["sub"] #Grab ID of current user  N.B email needs to be all lower case. 
            
            prompt_details = backend.get_prompts_for_tomrorow(handler_input.attributes_manager.session_attributes["url_heroku"],token,grab_alfred_id)
        except:
            speak_output = "I'm sorry, but we were unable to get your reminders for tomorrow. Please try again later."
        for j in range(len(prompt_details[0])):
            if j ==0:
                speak_output = speak_output + "You have a prompt to: {}, tomorrow at: {} ".format(prompt_details[0][0],backend.am_pm_speech(prompt_details[1][0]))
            if j > 0 and j != (len(prompt_details[0])-1):
                speak_output = speak_output + ",{} at {}".format(prompt_details[0][j],backend.am_pm_speech(prompt_details[1][j]))
            if j == (len(prompt_details[0]) -1) and (len(prompt_details[0]) != 1):
                speak_output = speak_output + ",and another to: {} at: {}".format(prompt_details[0][j],backend.am_pm_speech(prompt_details[1][j]))
                
                
        return handler_input.response_builder.speak(speak_output).response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #handler_input.attributes_manager.session_attributes["First_time"] = True # declare session variable to let intents know whether to guide user or not for future speeches 
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output="You first set reminders by saying: remind me to. For example: remind me to take my medication."
        handler_input.attributes_manager.session_attributes["First_time"] = True # declare session variable to let intents know whether to guide user or not for future speeches 
        try:
            if handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] ==False and handler_input.attributes_manager.session_attributes["user_confirmed_input"] ==False and handler_input.attributes_manager.session_attributes["user_confirmed_weekday_time"]==False:
                speak_output = "You can start setting a reminder by saying: remind me to take my medication, or: set a prompt to take my medication. Give it a try now!"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
        except:
            pass
        try:
            if handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] == True or handler_input.attributes_manager.session_attributes["user_confirmed_weekday_time"] == True:
                try:
                    if handler_input.attributes_manager.session_attributes["user_confirmed_input"] == False:
                        speak_output = "You have already set the date and time. You will now set a prompt to finish setting your reminder. For example, you can say: could I have a prompt to go to my appointment."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
        except:
            pass
        
        try:
            if handler_input.attributes_manager.session_attributes["input"] != None and handler_input.attributes_manager.session_attributes["user_confirmed_date_time"]==False and handler_input.attributes_manager.session_attributes["user_confirmed_weekday_time"] ==False:
                speak_output = "You have just set a reminder. You can now set a time and date, by saying for example: seven a.m. tomorrow."
        except:
            pass
        
        if handler_input.attributes_manager.session_attributes["user_confirmed_input"] == True:
            try:
                if handler_input.attributes_manager.session_attributes["date_only_provided"] != None and handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] == False:
                    speak_output = "You're almost there. you just need to set the time. For example, you can say: eight a.m"
            except:
                pass
            try:
                if handler_input.attributes_manager.session_attributes["weekday_only_provided"] != None and handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] == False:
                    speak_output = "You're almost there. you just need to set the time. For example, you can say: eight a.m"
            except:
                pass
            try:
                if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] == False:
                    speak_output = "You're almost there. you just need to set the date. For example you can say: next wednesday"
            except:
                pass
            
        try:
            if handler_input.attributes_manager.session_attributes["date_time_input_ready"] == True:
                speak_output = "You can simply say yes to confirm your prompt. Otherwise, you can say no and start again."
        except:
            pass
            
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)

class repeatsentenceIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("repeatsentenceintent")(handler_input)

    def handle(self, handler_input):
        speak_output = "repeat intent activated"
        try:
            speak_output = handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"]
        except:
            pass
        
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)



class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You have ended the Alfred skill. I hope to see you soon!"
        
        try:
            if handler_input.attributes_manager.session_attributes["First_time"] == True:
                #speak_output = "You have cancelled the Alfred skill. You can quickly start setting a reminder by saying: Alexa, tell alfred remind me to: followed by your prompt. See you later!"
                speak_output = "If you need assistance, you can always say help again. See you later!"
        except:
            pass

        return (handler_input.response_builder.speak(speak_output).response)

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "No intent isn't here yet. Sorry! also just saying the input returns an error. We'll fix that"
        reprompt = "I didn't catch that. What can I help you with?"
        return (handler_input.response_builder.speak(speech).ask(speech).response)

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response)

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speak_output = "I'm sorry, I had trouble doing what you asked. If you need some help. you can say: help to me, or: request help. Otherwise, you can  try setting a reminder again"
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(setreminderdescriptionIntentHandler())
sb.add_request_handler(yesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(whatpromptsIntentHandler())
sb.add_request_handler(datetimeIntentHandler())
sb.add_request_handler(repeatsentenceIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
lambda_handler = sb.lambda_handler()
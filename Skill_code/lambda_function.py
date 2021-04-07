# -*- coding: utf-8 -*-
# This is the main entry point of the backend service. 
# All the request data from the Alexa intent is received here and is supposed to be returned from this file only.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management, session persistence, api calls, and more.
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


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

###################Note calling weekdays_ = ask_utils.request_util.get_slot(handler_input, "weekdays")
#####when there is no slot in the intent will return None
######Note calling speak_output = "{}".format(handler_input.attributes_manager.session_attributes["weekdays"]) where the session variable was assigned to --> ask_utils.request_util.get_slot(handler_input, "weekdays")

# Every new handler class needs to be passed on to .add_request_handler() in the Skill Builder at the end	
class LaunchRequestHandler(AbstractRequestHandler):

    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #These variables must be declared below, otherwise calling them will cause an exception error. Calling a non-existent values will return NULL. 
        #handler_input.attributes_manager.session_attributes["First_time"] = False # declare session variable to let intents know whether to guide user or not for future interactions
        handler_input.attributes_manager.session_attributes["user_confirmed_input"] = False
        handler_input.attributes_manager.session_attributes["user_confirmed_weekday_time"] = False

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = '<speak> \
                        <voice name="Matthew"> \
                        Hello! My name is Alfred, and I am here to help you remember things. I can set, and give you reminders. \
                        </voice> \
                        </speak>' # Toset a reminder, you can say for example: remind me to: walk the dog."
                                  # You can also start with a date and time. As an example, you can say: set a reminder for 8 p.m, next thursday. Why don't you try it now?"
        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
        reprompt = '<speak> \
                    <voice name="Matthew"> \
                    If you need further guidance, you can say: help, or: I need assistance.
                    </voice> \
                    </speak>'
        return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)

#note calling a session attribute that wasnt initially declared, classifies the value as NULL or None --> very useful. 
class setreminderdescriptionIntentHandler(AbstractRequestHandler):
    """Handler for setreminderdescriptionIntent """
    def can_handle(self, handler_input):
        handler_input.attributes_manager.session_attributes["user_confirmed_input"] = True
        return ask_utils.is_intent_name("setremindertype")(handler_input)

    def handle(self, handler_input):
        #note calling a sllot value using ask_utils.request_util.get_slot(handler_input,~~) that wasnt initially declared classifies the value as NULL or None --> Potentially very useful for variable checks.
        
        # Fetch the title of the prompt from the user
        input_ = ask_utils.request_util.get_slot(handler_input, "input")
        handler_input.attributes_manager.session_attributes["input"] =input_.value
        
        try:
            if handler_input.attributes_manager.session_attributes["First_time"] == True and input_.value != None:
            # Could be useful to explain what happens here, e.g. in this case the user has opened Alexa x Alfred for the first time and has filled the input slot already.
                speak_output = "You've set a reminder to {}. You will now set the date and time. For example, you can try saying: remind me tomorrow at 7 a.m".format(input_.value)
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
            else:
                speak_output = "{}".format(handler_input.attributes_manager.session_attributes["First_time"])
        except:
            speak_output = "Thanks, what date and time would you like for your reminder?"
            handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
        
        try:
            if input_.value != None and handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] == True:
                try:
                    if handler_input.attributes_manager.session_attributes["time"] != None and handler_input.attributes_manager.session_attributes["date"] != None:
                        speak_output = "You have set a reminder to {}. for {}, at {}. Is that correct?".format(input_.value,handler_input.attributes_manager.session_attributes["date"],handler_input.attributes_manager.session_attributes["time"])
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
                
                try:
                    if handler_input.attributes_manager.session_attributes["time"] != None and handler_input.attributes_manager.session_attributes["weekdays"] != None:
                        speak_output = "you have set a reminder to {}. for next {}, at {}. Is that correct?".format(input_.value,handler_input.attributes_manager.session_attributes["weekdays"],handler_input.attributes_manager.session_attributes["time"])
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
        except:
            pass


        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["date_only_provided"] != None:
                speak_output = "you have set a reminder to {}. for {}, at {}. Is that correct?".format(input_.value,handler_input.attributes_manager.session_attributes["date_only_provided"],handler_input.attributes_manager.session_attributes["time_only_provided"])
        except:
            pass
        
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["weekday_only_provided"] != None:
                speak_output = "you have set a reminder to {}. for next {}, at {}. Is that correct?".format(input_.value,handler_input.attributes_manager.session_attributes["weekday_only_provided"],handler_input.attributes_manager.session_attributes["time_only_provided"])
        except:
            pass
        
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)


class datetimeIntentHandler(AbstractRequestHandler):
    """Handler for datetimeIntent"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] = True
        return ask_utils.is_intent_name("setdatetimeintent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Note: If variables below are not initially declared, they will be classified as NULL or None --> very useful.
        date_ =ask_utils.request_util.get_slot(handler_input, "date")
        time_ =ask_utils.request_util.get_slot(handler_input, "time")
        weekdays_ = ask_utils.request_util.get_slot(handler_input, "weekdays")
        input_ = ask_utils.request_util.get_slot(handler_input, "input")
        speak_output="To set a reminder, you can say for example: remind me to walk the dog. You can also start with a date and time. For example, you can say: set a reminder for 8 p.m next thursday. Would you like to try it now?"
        
        try:
            if date_.value != None and time_.value != None and handler_input.attributes_manager.session_attributes["user_confirmed_input"] == True:
                speak_output ="you have set a reminder to {}. for {}, at {}. Is that correct?".format(handler_input.attributes_manager.session_attributes["input"],time_.value,date_.value)
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["date"] = date_.value#
                handler_input.attributes_manager.session_attributes["time"] = time_.value#
            elif weekdays_.value != None and time_.value != None and  handler_input.attributes_manager.session_attributes["user_confirmed_input"] == True:
                speak_output ="You have set a reminder to: {}, for next {}, at {}. Is that correct?".format(handler_input.attributes_manager.session_attributes["input"],weekdays_.value,time_.value)
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["weekdays"] = weekdays_.value#
                handler_input.attributes_manager.session_attributes["time"] = time_.value#
            elif date_.value != None and time_.value != None:# and handler_input.attributes_manager.session_attributes["user_confirmed_input"] == False:#########
                speak_output = "Thank you. now. what would you like me to remind you about?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "Thank you now that you've set the date and time. You can now tell me what to remind you abou. For example, you can tell me: remind me to make lunch."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
                handler_input.attributes_manager.session_attributes["date"] = date_.value#
                handler_input.attributes_manager.session_attributes["time"] = time_.value#
                handler_input.attributes_manager.session_attributes["weekdays"] = weekdays_.value# this value will be set to NULL/None
        
        except:
            handler_input.attributes_manager.session_attributes["weekdays"] = weekdays_.value
            speak_output = "Thank you, now. what would you like me to remind you about?"
            handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
            try:
                if handler_input.attributes_manager.session_attributes["First_time"] == True:
                    speak_output = "Thank you, now that you've set the date and time. You can now tell me what to remind you about. As an example you can say: remind me to take my medicine"
                    handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
            except:
                pass
            handler_input.attributes_manager.session_attributes["date"] = date_.value
            handler_input.attributes_manager.session_attributes["time"] = time_.value
            handler_input.attributes_manager.session_attributes["weekdays"] = weekdays_.value
        try:
            if handler_input.attributes_manager.session_attributes["date_only_provided"] != None and time_.value != None:
                speak_output = "Thank you, now. what would you like me to remind you about?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["time"] = time_.value
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "Thank you, now that you've set the date and time. You can now tell me what to remind you about. As an example you can say: remind me to take my medicine"
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["time"] = time_.value
                except:
                    pass
                        
        except:
            pass
        
        try:
            if weekdays_.value != None and time_.value != None:
                speak_output = "Thank you, now. what would you like me to remind you about?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["time"] = time_.value
                
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "Thank you, now that you've set the date and time. You can now tell me what to remind you about. As an example you can say: remind me to take my medicine"
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["time"] = time_.value
                except:
                    pass
        except:
            pass
###########

        try:
            if date_.value != None and time_.value == None:
                speak_output = "Thanks, now. When would you like me to remind you?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["date_only_provided"] = date_.value
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output ="That's great. Now that you've set the date, could you please tell me the time? For example, you can say: 7 a.m"
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["date_only_provided"] = date_.value
                except:
                    pass
        except:
            pass
        
        try:
            if weekdays_.value != None and time_.value ==None:
                speak_output = "Thanks, now. what time would you like?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["weekday_only_provided"] = weekdays_.value
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output ="That's great. Now that you've set the date, could you please tell me the time? For example, you can say: seven a.m"
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["weekday_only_provided"] = weekdays_.value
                except:
                    pass
        except:
            pass

        try:
            if time_.value != None and weekdays_.value == None and date_.value == None:
                speak_output = "Thanks, now. what date would you like?"
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                handler_input.attributes_manager.session_attributes["time_only_provided"] = time_.value
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output ="That's great. Now that you've set the time, could you please tell me the date? For example, you can say: next week."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                        handler_input.attributes_manager.session_attributes["time_only_provided"] = time_.value
                except:
                    pass
        except:
            pass
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["weekday_only_provided"] != None:
                speak_output = "that's great. Now what reminder would you like?"
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "that's great. Now what reminder would you like? For example, you can say: remind me to buy bread"
                except:
                    pass
        except:
            pass
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["date_only_provided"] != None:
                speak_output = "that's great. Now what reminder would you like?"
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output = "that's great. Now what reminder would you like? For example, you can say: remind me to buy bread"
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
        except:
            pass
        
 ##########       
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["date_only_provided"] != None and handler_input.attributes_manager.session_attributes["input"] != None:
                
                speak_output = "You have set a reminder to {}. for {}, at {}. Is that correct? ".format(handler_input.attributes_manager.session_attributes["input"],handler_input.attributes_manager.session_attributes["date_only_provided"],handler_input.attributes_manager.session_attributes["time_only_provided"])
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
        except:
            pass
        
        try:
            if handler_input.attributes_manager.session_attributes["time_only_provided"] != None and handler_input.attributes_manager.session_attributes["weekday_only_provided"] != None and handler_input.attributes_manager.session_attributes["input"] != None:
                
                speak_output = "You have set a reminder to {}. for next {}, at {}. Is that correct? ".format(handler_input.attributes_manager.session_attributes["input"],handler_input.attributes_manager.session_attributes["weekday_only_provided"],handler_input.attributes_manager.session_attributes["time_only_provided"])
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
        except:
            pass
                        
                
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)



class yesIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        
        speak_output ="test"
        try:
            speak_output = "test 1 2 "
            if handler_input.attributes_manager.session_attributes["input"] != None and handler_input.attributes_manager.session_attributes["date"] != None and handler_input.attributes_manager.session_attributes["time"] != None:
                speak_output = "That's great. Your prompt now has been set."
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output ="That's great. Your prompt has been set. Next time, you can start setting a prompt by saying: Alexa, tell Alfred, remind me to {}. For further assistance, you can say: help.".format(handler_input.attributes_manager.session_attributes["input"])
                except:
                    pass
        except:
            pass
        
        try:
            if handler_input.attributes_manager.session_attributes["input"] != None and handler_input.attributes_manager.session_attributes["weekdays"] != None and handler_input.attributes_manager.session_attributes["time"] != None:
                speak_output = "That's great. Your prompt now has been set."
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                try:
                    if handler_input.attributes_manager.session_attributes["First_time"] == True:
                        speak_output ="That's great. Your prompt has been set. Next time, you can start setting a prompt by saying: Alexa, tell Alfred, remind me to {}. For further assistance, you can say: help.".format(handler_input.attributes_manager.session_attributes["input"])
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
        except:
            pass
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        handler_input.attributes_manager.session_attributes["First_time"] = True # declare session variable to let intents know whether to guide user or not for future speeches 
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output="test"
        try:
            if handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] ==False and handler_input.attributes_manager.session_attributes["user_confirmed_input"] ==False and handler_input.attributes_manager.session_attributes["user_confirmed_weekday_time"]==False:
                speak_output = "You can start setting a reminder by saying: remind me to take medicine. Or: set a prompt to: take my medicine. I will then ask you for the date and time."
                handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
        except:
            pass
        try:
            if handler_input.attributes_manager.session_attributes["user_confirmed_date_time"] == True or handler_input.attributes_manager.session_attributes["user_confirmed_weekday_time"] == True:
                try:
                    if handler_input.attributes_manager.session_attributes["user_confirmed_input"] == False:
                        speak_output = " You've already set the date and time. You will now set a prompt to finish setting your reminder. As an example, You can say. could I have a prompt to: go to my appointment."
                        handler_input.attributes_manager.session_attributes["save_phrase_for_repeat"] = speak_output
                except:
                    pass
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
                speak_output = "You have cancelled the Alfred skill. You can quickly start setting a reminder by saying: Alexa, tell alfred to remind me to: followed by your prompt. See you later!"
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
        speech = "Hmm, I'm not sure. You can say: remind me to do something, or: Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"
        return (handler_input.response_builder.speak(speech).ask(reprompt).response)

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
sb.add_request_handler(datetimeIntentHandler())
sb.add_request_handler(repeatsentenceIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(IntentReflectorHandler()) # IntentReflectorHandler must be last so it doesn't override custom intent handlers
lambda_handler = sb.lambda_handler()

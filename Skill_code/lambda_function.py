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


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)




class LaunchRequestHandler(AbstractRequestHandler):

    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        handler_input.attributes_manager.session_attributes["input"] = None # initialise -reminder- value in session as None upon launch
        handler_input.attributes_manager.session_attributes["time"] = None # similarly, set the time attribute in session as None for now
        handler_input.attributes_manager.session_attributes["date"] = None # similarly, set the Data attribute in session as None for now
        handler_input.attributes_manager.session_attributes["weekdays"] = None # similarly, set the Data attribute in session as None for now
        handler_input.attributes_manager.session_attributes["First_time"] = True # declare session variable to let intents know whether to guide user or not for future speeches 
        speak_output = "Hello! My name is Alfred, and I'm here to help you remember things better. As an example, you can say: remind me to: go for a walk. Why don't you set your own prompt now?"# You can also start with a date and time. As an example, you can say: set a reminder for 8 p.m, next thursday. Why don't you try it now?"
        reprompt = "If you need further guidance. you can simply say: help. Or: I need assistance"
        return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)





class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        handler_input.attributes_manager.session_attributes["First_time"] = True # declare session variable to let intents know whether to guide user or not for future speeches 
        speak_output = "You can set prompts of your own. As an example, you can say. set a reminder to: write an email to a friend. Another example would be: remind me to prepare lunch for tomorrow. Following from this, I will ask you for both the date and time. "
        reprompt = "Why don't you first try to set a prompt by saying. Set a prompt to: get some fresh air. I'll guide you along the way."
        if handler_input.attributes_manager.session_attributes["input"] is not None: # if user has set a prompt activity, but wants help for date + time, run this block
            speak_output = "A date, and time, for your prompt: {}, must be added. As an example, you can say: remind me at eight p.m, next wednesday".format(handler_input.attributes_manager.session_attributes["input"])
            reprompt = "A date and time for your prompt: {}, must be added. As an example, you can say: remind me at eight p.m, next wednesday"

        return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)

#note calling a session attribute that wasnt initially declared, classifies the value as NULL or None --> very useful. 
class testIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("reminderIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        input_ = ask_utils.request_util.get_slot(handler_input, "input")
        date_ =ask_utils.request_util.get_slot(handler_input, "date")
        time_ =ask_utils.request_util.get_slot(handler_input, "time")
        weekdays_ = ask_utils.request_util.get_slot(handler_input, "weekdays")
        speak_output = ""

        if time_.value != None and date_.value != None:
            speak_output = "You have set a reminder for: {}, at {}. Is that correct?".format(date_.value,time_.value)#,date_.value,time_.value)
            handler_input.attributes_manager.session_attributes["date"] = date_.value # save for other intents later
            handler_input.attributes_manager.session_attributes["time"] = time_.value # save for other intents later
        elif weekdays_.value != None and time_.value != None:
            speak_output = "You would like a reminder for next {}, at {}. Is that correct?".format(weekdays_.value,time_.value)
            handler_input.attributes_manager.session_attributes["weekdays"] = weekdays_.value # save for other intents later
            handler_input.attributes_manager.session_attributes["time"] = time_.value # save for other intents later
        elif time_.value == None and date_.value == None and input_.value != None:
            speak_output = "You would like a reminder to: {}. Is that correct?".format(input_.value)
        handler_input.attributes_manager.session_attributes["input"] = input_.value # save for other intents

        
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)

class yesIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        input_ = handler_input.attributes_manager.session_attributes["input"]
        date_ = handler_input.attributes_manager.session_attributes["date"]
        time_ = handler_input.attributes_manager.session_attributes["time"]
        weekdays_ = handler_input.attributes_manager.session_attributes["weekdays"]
        first_time_ = handler_input.attributes_manager.session_attributes["First_time"] #we set this before as True if the user ran through the tutorial. That way, we can change future speech outputs to aid them in future prompt requests
        
        speech_output = "I'm sorry. I didn't catch that. As an example, you can say: remind me to prepare tomorrow's meal. You can also say: set me a reminder for: next wednesday at 11 a.m"
        
        
        if input_ != None and date_ == None and time_ == None:
            print("hi")
            if first_time_ == True:
                speak_output = "That's great. what date and time would you like?"
                reprompt = "Now that you've confirmed your prompt. Why don't you suggest a date and time?" 
        return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)




class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"
        
        if handler_input.attributes_manager.session_attributes["First_time"] == True: #condition for test_variable
            speech = "I'm sorry. I didn't catch that. As an example, you can say: remind me to prepare tomorrow's meal. You can also say: set me a reminder for: next wednesday at 11 a.m"
            reprompt = "As an example, you can say: create a reminder for me next sunday at six forty five a.m"
            
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
                .response
        )


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

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(testIntentHandler())
sb.add_request_handler(yesIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
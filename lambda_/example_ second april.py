# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value
import ask_sdk_core.utils as ask_utils

from ask_sdk_model import Response,DialogState

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
        handler_input.attributes_manager.session_attributes["First_time"] = True # declare session variable to let intents know whether to guide user or not
        speak_output = "Hello, My name is Alfred, and I'm here to help you remember things better. As an example. you can say: remind me to go for a walk. And we'll create a prompt for you to: go for a walk. Why don't you try it now?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class testIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("reminder")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        input_ = ask_utils.request_util.get_slot(handler_input, "input")
        date_ =ask_utils.request_util.get_slot(handler_input, "date")
        time_ =ask_utils.request_util.get_slot(handler_input, "time")
        if time_.value != None and date_.value != None:
            speak_output = "You have set a reminder to {}, at test, test. Is that correct?".format(input_.value)#,date_.value,time_.value)
            handler_input.attributes_manager.session_attributes["input"] = input_.value # save for other intents
            handler_input.attributes_manager.session_attributes["date"] = date_.value # save for other intents
            handler_input.attributes_manager.session_attributes["time"] = time_.value # save for other intents
        else:
            speak_output = "You have set a reminder to: {}. Is that correct?".format(input_.value)
        handler_input.attributes_manager.session_attributes["input"] = input_.value # save for other intents

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response)

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
        #first_time_ = handler_input.attributes_manager.session_attributes["First_time"] 
        #if input_ == None: # check if there's even a value in the input slot
        #    speak_output = "empty slot detected"
        
        if date_.value == None and time_.value == None:
            speak_output = "That's great. Now. As an example, you can say: tell alfred ex, remind me to {} at six a.m tomorrow".format(input_.value)
            #first_time_ = first_time_ + 1

            

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




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

        return handler_input.response_builder.speak(speech).ask(reprompt).response

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

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

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
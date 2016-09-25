"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import json
import requests
from datetime import datetime, timedelta

address = []
time2 = []
group_name = []
location_name = []

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------

#Asks user for location
def GetWelcomeResponse():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa tech event finder." \
                    "If you would like to find tech related events please say, " \
                    "Find events"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "If you would like to find tech related events please say, " \
                    "Find events"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "For further information please refer to meetup.com" \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


#api call w/location to find events
#def set_location_session(intent, session):
def EventIntent(intent, session):

    class BlankDict(dict):
        def __missing__(self, key):
            return None
    def datetime_from_millis(millis, epoch=datetime(1970,1,1)):
        return epoch + timedelta(milliseconds=millis)
    baseurl = "https://api.meetup.com"
    full_url = baseurl + "/find/locations"
    url7 = "https://api.meetup.com/2/open_events?zip=10001&and_text=False&offset=0&city=new+york+city&format=json&limited_events=False&topic=technology&photo-host=public&page=5&radius=25.0&desc=False&status=upcoming&sig_id=186421735&sig=a596ac6fe2ab623d91eb867a389de48b65f59ab2"
    results = requests.get(url7, verify=False)
    json_contents = json.loads(results.content, object_hook=BlankDict)

    for item in json_contents["results"]:
        time = item["time"]
        time2.append(datetime_from_millis(time))
        group_name.append(item["group"]["name"])
        if item["venue"] is None:
            pass
            address.append("No available address.")
            location_name.append("No available venue name.")
        else:
            address.append(item["venue"]["address_1"])
            location_name.append(item["venue"]["name"])

    if 'location' in intent['slots']:
        event = intent['slots']['location']['value']
        session_attributes = create_event_attributes(location)
        speech_output = eventName + "is meeting at " + time \

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, should_end_session))

#states all the events
def GetEventInfo(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "location" in session.get('attributes', {}) and "EventIntent" in session.get('attributes', {}):
        event = session['attributes']['location'] ['eventName']

        should_end_session = True
    else:
        should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], 'Hello', reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

#goes through the intents
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetEventInfo":
        return EventIntent(intent, session)
    if intent_name == "EventsIntent":
        return GetEventInfo(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

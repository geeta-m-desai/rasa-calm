# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.voice_handling import receive_and_speak_response


class HelloWorld(Action):

    def name(self) -> Text:
        return "hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> list[str]:

        # dispatcher.utter_message(text="Hello World! from MitramCares!!")
        text = "Warm greetings from MitramCares! I'm your friendly helper. How can I make things easier for you today?"
        dispatcher.utter_message(text)
        # receive_and_speak_response(text)
        return []

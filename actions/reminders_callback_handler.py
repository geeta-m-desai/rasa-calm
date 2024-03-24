from typing import Text
from rasa_sdk import Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.types import DomainDict


class ActionNotifyMedication(Action):
    def name(self) -> Text:
        return "action_notify_medication"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> list[EventType]:
        try:
            print("ActionNotifyMedication is triggered ----> ")
            dispatcher.utter_message(response="utter_time_for_medication")
            return []

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

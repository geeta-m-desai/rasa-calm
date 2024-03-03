from rasa_sdk import Action
from rasa_sdk.events import SlotSet


class ActionUtterAnswer(Action):

    def name(self) -> Text:
        return "utter_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        answer = tracker.get_slot("answer")  # Get the answer from the slot
        dispatcher.utter_message(text=answer)

        return []  # End the action

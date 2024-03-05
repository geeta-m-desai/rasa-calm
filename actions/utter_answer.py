from rasa_sdk import Action


class ActionUtterAnswer(Action):

    def name(self):
        return "action_utter_answer"

    def run(self, dispatcher,
            tracker,
            domain):
        answer = tracker.get_slot("answer")  # Get the answer from the slot
        dispatcher.utter_message(text=answer)

        return []  # End the action

import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action
from rasa_sdk.events import ReminderScheduled
from rasa_sdk.executor import CollectingDispatcher, Tracker


class ActionScheduleMedicationReminder(Action):
    def name(self) -> Text:
        return "action_schedule_medication_reminder"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        try:
            dispatcher.utter_message("I will remind you in 5 seconds.")

            date = datetime.datetime.now() + datetime.timedelta(minutes=1)
            entities = tracker.latest_message.get("entities")
            print("entities ===> ", entities)

            reminder = ReminderScheduled(
                "EXTERNAL_reminder_callback",
                trigger_date_time=date,
                entities=entities,
                name="my_reminder",
                kill_on_user_message=False,
            )
            print("reminder ===> ", reminder)
            return [reminder]
        except Exception as e:
            dispatcher.utter_message(text=f"An exception occurred: {str(e)}")
            return []

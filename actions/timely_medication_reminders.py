import datetime
import pytz
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset, ReminderScheduled, SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionScheduleMedicationReminder(Action):
    def name(self) -> Text:
        return "action_schedule_medication_reminder"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            dispatcher.utter_message("I will remind you in 5 seconds.")

            calcutta = pytz.timezone('Asia/Calcutta')
            date = datetime.datetime.now(calcutta) + datetime.timedelta(seconds=10)
            reminder = ReminderScheduled(
                "EXTERNAL_revert",
                trigger_date_time=date,
                name="medication_reminder",
                kill_on_user_message=False,
                timestamp=datetime.datetime.now(calcutta).timestamp()
            )
            print("reminder ===> ", reminder)
            return [reminder, SlotSet('reminder_callback_pending', True)]

        except Exception as e:
            print("execution exception --->  ", e)
            return []

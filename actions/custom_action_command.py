import os
import openai
from rasa_sdk import Action


class CustomKnowledgeAnswerCommand(Action):
    def name(self):
        return "action_custom_knowledge_answer"

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def run(self, dispatcher, tracker, domain):

        user_query = tracker.latest_message  # Assuming the query is in the latest message

        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # Replace with your desired model
                prompt=user_query,
                max_tokens=100,  # Adjust as needed
                n=1,
                stop=None,
                temperature=0.5,  # Adjust for creativity
            )

            answer = response.choices[0].text.strip()
            dispatcher.utter_message(text=answer)

        except openai.error.APIError as e:
            dispatcher.utter_message(text="Error fetching answer: {e}")

        return []

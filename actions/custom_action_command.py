import os


import openai
from rasa_sdk import Action


class CustomKnowledgeAnswerCommand(Action):
    def name(self):
        return "action_custom_knowledge_answer"

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def run(self, dispatcher, tracker, domain):

        user_query = tracker.latest_message.get('text')  # Assuming the query is in the latest message

        try:
            # Convert to openAI messages format
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query},
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            answer = response['choices'][0]['message']['content']
            print("answer", answer)
            dispatcher.utter_message(text=answer)

        except openai.error.APIError as e:
            dispatcher.utter_message(text="Error fetching answer: {e}")

        return []

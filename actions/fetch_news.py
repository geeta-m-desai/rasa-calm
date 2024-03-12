import requests
from rasa_sdk import Action
import pdb

from actions.voice_handling import receive_and_speak_response


class ActionFetchNews(Action):
    def name(self):
        return "action_fetch_news"

    def run(self, dispatcher, tracker, domain):
        api_key = "47182d0062c844b49681ffeaa7b8626f"
        base_url = "https://newsapi.org/v2/"

        # Get preferences or use defaults
        # source = tracker.get_slot("source")
        country = "in"  # Example default
        category = "general"  # Example default

        # # Choose endpoint based on preferences
        # if source:
        #     endpoint = "top-headlines?sources={}"
        # else:
        #     endpoint = "everything?q={}"
        endpoint = "/everything?q={}"
        # Construct parameters (See NewsAPI docs for more options)
        params = {
            "apiKey": api_key,
            "country": country,
            "category": category
        }

        # Send the API request
        # url = base_url + endpoint.format(source)
        url = "https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey=47182d0062c844b49681ffeaa7b8626f"
        response = requests.get(url, verify=False)
        # pdb.set_trace()
        if response.status_code == 200:
            data = response.json()
            if data["totalResults"] == 0:
                dispatcher.utter_message(text="Sorry, no articles found for your criteria.")
            else:
                summary = "Here are some top headlines:\n"
                for article in data["articles"][:3]:
                    summary += f"- {article['title']}: {article['description']}\n"
                dispatcher.utter_message(text=summary)
                # receive_and_speak_response(summary)
        else:
            dispatcher.utter_message(text="Sorry, I'm having trouble getting the news right now.")

        return []

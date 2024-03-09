import requests
from rasa_sdk import Action


class ActionFetchWeather(Action):
    def name(self):
        return "action_fetch_weather"

    def run(self, dispatcher, tracker, domain):
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?q=Pune&appid=39f4b1263d75a62ab53287225fe1f5e2')
        weather_data = response.json()
        print("weather_data", weather_data)
        if response.status_code == 200:
            dispatcher.utter_message(
                text=f"Weather updates: {weather_data['weather'][0]['description']} with temperature {weather_data['main']['temp']} Kelvin")
        else:
            dispatcher.utter_message(text="Unable to fetch weather updates at the moment. Please try again later.")

        return []

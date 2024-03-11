import os
from gtts import gTTS
import espeakng
import speech_recognition as sr
import requests
from googletrans import Translator

ACTION_ENDPOINT_URL = "http://localhost:5005/webhooks/rest/webhook"


def listen_and_send_to_rasa():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak (or press Enter to skip):")
        try:
            audio = r.listen(source, timeout=2, phrase_time_limit=2)
            text = r.recognize_google(audio, language="en-US")
            print("Recognized ", text)
            data = {"message": text}
            response = requests.post(ACTION_ENDPOINT_URL, json=data)
            print("response --> ", response.json())
            return response
        except sr.WaitTimeoutError:
            print("Please speak. Could not hear you clearly.")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error from recognition service; {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending to Rasa endpoint; {e}")


def receive_and_speak_response_mac(response_text):
    os.system(f"say '{response_text}'")  # macOS TTS


def receive_and_speak_response(response_text):
    print("response_text ", response_text)
    voice = espeakng.Speaker(gender='female', voice='en')  # Customize if needed
    voice.say(response_text)


# Example usage
if __name__ == "__main__":
    listen_and_send_to_rasa()

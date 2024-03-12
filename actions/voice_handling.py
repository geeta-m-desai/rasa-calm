import os

import espeakng
import requests
import speech_recognition as sr

from actions.translate_text import translate_text

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


def receive_and_speak_response_old(response_text, language="en"):
    print("response_text ", response_text)
    translated_text = translate_text(response_text, language)
    print("translated_text ", translated_text)
    voice = espeakng.Speaker()
    voice.voice = language
    voice.say(translated_text)


import os
from google.cloud import texttospeech


def receive_and_speak_response(response_text, language="mr-IN"):
    # Directly set the environment variable within the function
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/geetadesai/Downloads/mitramcares-tts-e799c0c11b42.json"
    translated_text = translate_text(response_text,language)
    # Initialize Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Configure voice and text
    input_text = texttospeech.SynthesisInput(text=translated_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language,
        # Optionally select a specific voice name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Synthesize the audio response
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Play the audio (Example using 'playsound')
    try:
        import playsound
        with open("output.mp3", "wb") as out:
            out.write(response.audio_content)
        playsound.playsound("output.mp3")
    except ImportError:
        print("Could not import playsound. Find an alternative way to play the audio output.")


# Example usage
if __name__ == "__main__":
    listen_and_send_to_rasa()

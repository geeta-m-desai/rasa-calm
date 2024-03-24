import os
from typing import Optional

import requests
import speech_recognition as sr
from google.cloud import texttospeech
import time
from actions.translate_text import translate_text

ACTION_ENDPOINT_URL = "http://localhost:5005/webhooks/rest/webhook"

r = sr.Recognizer()


def audio_chunk_send_to_rasa(audio_chunk: bytes, sample_rate: int = 44100, sample_width: int = 2,
                             language: Optional[str] = "kn-IN"):
    try:
        start_time = time.time()
        audio = sr.AudioData(audio_chunk, sample_rate, sample_width)
        end_time = time.time()
        print(f"Conversion took -1(STT)"
              f" -->: {end_time - start_time:.2f} seconds")
        start_time = time.time()
        text = r.recognize_google(audio, language=language)
        end_time = time.time()

        print(f"Conversion took -1.1(STT)"
              f" -->: {end_time - start_time:.2f} seconds")
        print("Recognized ", text)
        data = {"message": text}
        start_time = time.time()
        response = requests.post(ACTION_ENDPOINT_URL, json=data)
        response_content = response.json()  # Extract response content
        end_time = time.time()
        print(f"Conversion took -2(Rasa Response) -->: {end_time - start_time:.2f} seconds")
        print("response_content --> ", response_content[0]['text'])
        audio_response = receive_and_return_response(response_content[0]['text'], language)
        return audio_response

    except sr.WaitTimeoutError:
        print("Please speak. Could not hear you clearly.")
    except sr.UnknownValueError as e:
        print(f"Could not understand audio; {e}")
    except sr.RequestError as e:
        print(f"Error from recognition service; {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending to Rasa endpoint; {e}")


def listen_and_send_to_rasa():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak (or press Enter to skip):")
        try:
            audio = r.listen(source, timeout=2, phrase_time_limit=3)
            text = r.recognize_google(audio, language="en-US")
            print("Recognized ", text)
            data = {"message": text}
            response = requests.post(ACTION_ENDPOINT_URL, json=data)
            response_content = response.json()  # Extract response content
            print("response_content --> ", response_content)
            return response_content  # Return response content instead of the response object
        except sr.WaitTimeoutError:
            print("Please speak. Could not hear you clearly.")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error from recognition service; {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending to Rasa endpoint; {e}")


def receive_and_return_response(response_text, language="kn-IN"):
    # Directly set the environment variable within the function
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/geetadesai/Downloads/ultra-palisade-417016-a58005ad54b8.json"
    start_time = time.time()
    translated_text = translate_text(response_text, language)
    end_time = time.time()
    print(f"Conversion took -3 (Translation)-->: {end_time - start_time:.2f} seconds")
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
    start_time = time.time()
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    end_time = time.time()
    print(f"Conversion took -4(TTS) -->: {end_time - start_time:.2f} seconds")
    return response.audio_content


def receive_and_speak_response(response_text, language="mr-IN"):
    # Directly set the environment variable within the function
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/geetadesai/Downloads/ultra-palisade-417016-a58005ad54b8.json"
    translated_text = translate_text(response_text, language)
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

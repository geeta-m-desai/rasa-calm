from googletrans import Translator


def translate_text_old(text, target_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        print("Google Translate Response:", translation)
        return translation.text
    except Exception as e:
        print(f"Translation Error: {e}")
        return None  # Or a default value


import os
from google.cloud import translate_v2 as translate


def translate_text(text, target_language):
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/geetadesai/Downloads/mitramcares-tts-e799c0c11b42.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/geetadesai/Downloads/ultra-palisade-417016-a58005ad54b8.json"
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']


def main():
    text_to_translate = "Hello World! from MitramCares!! Is there anything I can help you with today?"
    target_language = "kn-IN"
    translated_text = translate_text(text_to_translate, target_language)
    print(f"Translated Text: {translated_text}")


if __name__ == "__main__":
    main()

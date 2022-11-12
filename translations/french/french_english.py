from google.cloud import translate_v2

def translate_english_french(word):
    translate_client = translate_v2.Client()
    return translate_client.translate(word, target_language="en-US")['translatedText']

from google.cloud import translate_v2


def five_word_translator(words):
    return_words = []
    translate_client = translate_v2.Client()
    for word in words:
        return_words.append({
            'English': word,
            "French": translate_client.translate(word, target_language="fr")['translatedText'],
            "Spanish": translate_client.translate(word, target_language="es")['translatedText'],
            "Italian": translate_client.translate(word, target_language="it")['translatedText'],
            "German": translate_client.translate(word, target_language="de")['translatedText'],
            "Russian": translate_client.translate(word, target_language="ru")['translatedText'],
            "Arabic": translate_client.translate(word, target_language="ar")['translatedText'],
            "Mandarin": translate_client.translate(word, target_language="zh")['translatedText'],
            "Estonian": translate_client.translate(word, target_language="et")['translatedText'],
            "Japanese": translate_client.translate(word, target_language="ja")['translatedText'],
            "Korean": translate_client.translate(word, target_language="ko")['translatedText'],
        })
    return return_words
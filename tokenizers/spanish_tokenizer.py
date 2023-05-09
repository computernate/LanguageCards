from bs4 import BeautifulSoup
import requests
from translations.french.french_all import get_french_translations
from tokenizers.spanish_exceptions import checkException
from google.cloud import translate_v2
import os
import spacy


def tokenize(word):
    returnWords = []

    translate_client = translate_v2.Client()
    translation = translate_client.translate(word, target_language="en-US")['translatedText']

    exception = checkException(word, translation)
    if (exception): return exception

    nlp = spacy.load('es_core_news_md')
    initial_tag = nlp(word)
    for token in initial_tag:
        print(print(token.text, token.lemma_, token.tag_, token.dep_))


if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "D:/nater/Documents/LanguageCards/google_api_credentials.json"
    # Words to add manually:
    # test = "El Athletic Club, popularmente conocido también como Athletic de Bilbao o simplemente Athletic, es un club de fútbol de la villa de Bilbao, País Vasco, España"
    test = "La banda sonora de la película está compuesta por Hiroyuki Sawano"
    for item in test.lower().split(' '):
        try:
            print(tokenize(item))

        except Exception as e:
            print('ERROR')
            print(e)

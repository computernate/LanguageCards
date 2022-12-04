
from db_functions import *
import requests
from google.cloud import translate_v2
from bs4 import BeautifulSoup
import re

def get_cards_fra(all_words, conn):
  translate_client = translate_v2.Client()
  return_object = []
  for word in all_words:
    if word == "":
      continue
    word = word.strip()
    split_word=word.split(',')
    word = split_word[0].strip()


    db_word = get_word("FR", word, conn)
    if db_word:
      db_word=db_word[0]
      translation = db_word[4]
      if len(split_word)>1: translation = split_word[1]
      word_object = {
        "language":"FR",
        "word":db_word[2],
        "pronunciation": db_word[3],
        "translation": translation,
        "t_sentence": db_word[5],
        "e_sentence": db_word[6],
        "level": db_word[7],
      }
      return_object.append(word_object)
      continue
    else:

      trans = ""
      #get translation
      try:
        trans=split_word[1]
      except:
        trans = translate_client.translate(word, target_language="en-US")['translatedText']

      #Get soup
      dictionary_data = requests.get(f"https://www.kikiladi.com/citation/{word}.html")
      soup = BeautifulSoup(dictionary_data.text, 'html.parser')

      sentences = soup.select('ul.citation')

      f_sentence = ""
      e_sentence = ""
      for child in sentences:
        try:
          f_sentence_dirty = child.text
          f_sentence = re.sub('<.*?>', '', f_sentence_dirty)
          e_sentence = translate_client.translate(f_sentence, target_language="en-US")['translatedText']
        except:
          continue
        if(e_sentence != "" and len(e_sentence) > 2 and len(e_sentence) < 200 and len(f_sentence.split(" "))>3):
          break

      word_object = {
        "language":"FR",
        "word":word,
        "pronunciation": "",
        "translation": trans,
        "t_sentence": f_sentence,
        "e_sentence": e_sentence,
        "level": "F",
      }
      insert_word(conn, word_object)
      return_object.append(word_object)
  return return_object

from db_functions import *
import requests
from bs4 import BeautifulSoup

def get_cards_esp(all_words, conn):
  return_object = []
  for word in all_words:
    if word == "":
      continue
    word = word.strip()
    split_word=word.split(',')
    word = split_word[0].strip()

    db_word = get_word("SP", word, conn)
    if db_word:
      db_word=db_word[0]
      translation = db_word[4]
      if len(split_word)>1: translation = split_word[1]
      word_object = {
        "language":"SP",
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
      #Get soup
      dictionary_data = requests.get("https://www.spanishdict.com/translate/{}".format(word))
      soup = BeautifulSoup(dictionary_data.text, 'html.parser')

      trans = ""
      #get translation
      try:
        trans=split_word[1]
      except:
        all_trans = soup.select('a[href^="/translate"][lang="en"]')
        for translation in all_trans:
          trans+="{}, ".format(translation.string)
        trans.strip(", ")
      #print(soup)
      sentences = soup.select('.QkSyASiy')

      s_sentence = ""
      e_sentence = ""
      for child in sentences:
        s_sentence = child.select_one('.S7halQ2C').text
        e_sentence = child.select_one('.msZ0iHzp').text
        if(e_sentence != "" and len(e_sentence) > 2 and len(e_sentence) < 200):
          break

      word_object = {
        "language":"SP",
        "word":word,
        "pronunciation": "",
        "translation": trans,
        "t_sentence": s_sentence,
        "e_sentence": e_sentence,
        "level": "S",
      }
      insert_word(conn, word_object)
      return_object.append(word_object)

  return return_object
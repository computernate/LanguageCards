import json

from db_functions import *
import requests
from bs4 import BeautifulSoup

def get_cards_jap(all_words, conn):
  return_object = []
  for word in all_words:
    if word == "":
      continue
    word = word.strip()
    split_word=word.split(',')
    word = split_word[0].strip()
    print(word)

    db_word = get_word("JP", word, conn)
    if db_word:
      db_word=db_word[0]
      translation = db_word[4]
      if len(split_word)>1: translation = split_word[1]
      word_object = {
        "language":"JP",
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
      #Get hiragana
      post_data = {
        "app_id": "fa0a9b5f79929cd507350044f56e6c0a68e47a9c10d0154513e85cd8747555ec", "sentence": word,
        "output_type": "hiragana"
      }
      hira_data = requests.post("https://labs.goo.ne.jp/api/hiragana", data=post_data)
      try:
        hira = json.loads(hira_data.text)['converted']
      except:
        hira = ""
      level = "0"
      #Get translation
      try:
        trans=split_word[1]
      except:
        trans_data = requests.get("http://beta.jisho.org/api/v1/search/words?keyword={}".format(word))
        trans = ', '.join(json.loads(trans_data.text)['data'][0]['senses'][0]['english_definitions'])
        if len(json.loads(trans_data.text)['data'][0]['jlpt']) > 0: level = json.loads(trans_data.text)['data'][0]['jlpt'][0][-1]

      #Get sentence
      jisho_data = requests.get("https://jisho.org/search/{}%20%23sentences".format(word))
      soup = BeautifulSoup(jisho_data.text, 'html.parser')
      sentence = soup.find(class_="sentences")

      e_sentence = ""
      try:
        for child in sentence.children:
          if len(child) < 2: continue
          j_sentence_raw = child.find(class_='japanese_sentence').find_all("li")
          j_sentence=""
          for li in j_sentence_raw:
            j_sentence+=li.find_all("span")[-1].string
          if len(j_sentence)<40:
            e_sentence=child.find(class_='english').string
            break
      except:
        pass

      if e_sentence=="": j_sentence=""

      word_object = {
        "language":"JP",
        "word":word,
        "pronunciation": hira,
        "translation": trans,
        "t_sentence": j_sentence,
        "e_sentence": e_sentence,
        "level": level,
      }
      insert_word(conn, word_object)
      return_object.append(word_object)

  return return_object

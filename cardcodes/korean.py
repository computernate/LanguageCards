
import requests
from db_functions import *
from google.cloud import translate_v2
from bs4 import BeautifulSoup

def get_korean_cards(all_words, conn):
  return_object = []
  translate_client = translate_v2.Client()
  for word in all_words:
    if word == "":
      continue
    word = word.strip()
    split_word=word.split(',')
    word = split_word[0].strip()

    db_word = get_word("KR", word, conn)
    if db_word:
      db_word=db_word[0]
      translation = db_word[4]
      if len(split_word)>1: translation = split_word[1]
      word_object = {
        "language":"KR",
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

      if len(split_word)==1: trans = translate_client.translate(word, target_language="en-US")['translatedText']
      else: trans = split_word[1]
      try:
        sentence_data = requests.get(f'https://www.ybmallinall.com/styleV2/dicview.asp?kwdseq=0&kwdseq2=0&DictCategory=DictAll&DictNum=0&ById=0&PageSize=5&StartNum=0&GroupMode=0&cmd=0&kwd={word}&x=0&y=0')
        soup = BeautifulSoup(sentence_data.text, 'html.parser')
        e_sentence = soup.select_one('div.DictResultEngSnt .Word').string
        k_sentence = soup.select_one('div.DictResultEngSnt .Example').string
      except:
        e_sentence = ""
        k_sentence = ""
      word_object = {
        "language":"KR",
        "word":word,
        "pronunciation": "",
        "translation": trans,
        "t_sentence": k_sentence,
        "e_sentence": e_sentence,
        "level": "",
      }
      insert_word(conn, word_object)
      return_object.append(word_object)
  return return_object

from db_functions import *
import requests
from bs4 import BeautifulSoup

def get_chinese(all_words, conn):
  return_object = []
  for word in all_words:
    if word == "":
      continue
    word = word.strip()
    split_word=word.split(',')
    word = split_word[0].strip()

    db_word = get_word("MD", word, conn)
    if db_word:
      db_word=db_word[0]
      translation = db_word[4]
      if len(split_word)>1: translation = split_word[1]
      word_object = {
        "language":"MD",
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


      dictionary_data = requests.get("https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define={}".format(word))
      soup = BeautifulSoup(dictionary_data.text, 'html.parser')

      c_sentence = ""
      e_sentence = ""
      pinyin = ""
      trans = ""

      all_entries = soup.select('li.entry')
      for entry in all_entries:
        entry_word = ""
        word_soup = entry.select('span.word:not(.trad) a')

        for word_part in word_soup:
          entry_word+=word_part.string
        if word == entry_word:
          try:
            trans=split_word[1]
          except:
            trans = entry.select_one('div.meaning').string.replace('\n', ', ')

          pinyin = entry.select_one('span.pinyin').string
          try:
            trad = entry.select_one('span.word.trad a').string
          except:
            trad = ""
          if entry.select_one('a.show_examples'):
            sentences_url = entry.select_one('a.show_examples')['href']
            sentence_data = requests.get("https://chinese.yabla.com/chinese-english-pinyin-dictionary.php"+sentences_url.format(word))
            sentence_soup = BeautifulSoup(sentence_data.text, 'html.parser')

            all_sentences = sentence_soup.select('div.example_text')
            for sentence in all_sentences:
              e_sentence = sentence.select_one('div.en').string
              if(len(e_sentence)<200):
                c_sentence = ""
                c_soup = sentence.select('div.zh_word span.zh_CN')
                for c in c_soup:
                  c_sentence += c.string
                break
          break


      #sentences = soup.select('div.translation__example')
      # for child in sentences:
      #   c_sentence = child.select_one('p[lang=zh]').string
      #   e_sentence = child.select_one('p.ex-mean span').string
      #   if(e_sentence != "" and len(e_sentence) > 2 and len(e_sentence) < 200):
      #     break

      if trad:
        word = "{} ({})".format(word, trad)
      word_object = {
        "language":"MD",
        "word":word,
        "pronunciation": pinyin,
        "translation": trans,
        "t_sentence": c_sentence,
        "e_sentence": e_sentence,
        "level": "",
      }
      insert_word(conn, word_object)
      return_object.append(word_object)
  return return_object
"""
Serves files out of its current directory
Dosen't handle POST request
"""

from flask import Flask, render_template, request
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('card_create.html')

@app.route('/get_cards', methods=['POST'])
def get_cards_all():
  return_object = []
  return_object += get_cards_fra(request.get_json()['french'])
  return_object += get_cards_esp(request.get_json()['spanish'])
  return_object += get_cards_jap(request.get_json()['japanese'])
  return_object += get_chinese(request.get_json()['chinese'])
  print(return_object)
  return json.dumps(return_object)

def get_cards_jap(all_words):
  return_object = []
  for word in all_words:
    print(word)
    if word == "":
      continue
    word = word.strip()
    split_word=word.split(',')
    word = split_word[0].strip()

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

    return_object.append({
      "word":word,
      "pronunciation": hira,
      "translation": trans,
      "t_sentence": j_sentence,
      "e_sentence": e_sentence,
      "level": level,
    })

  return return_object

def get_cards_esp(all_words):
  return_object = []
  for word in all_words:
    print(word)
    if word == "":
      continue
    word = word.strip()
    split_word=word.split(',')
    word = split_word[0].strip()

    #Get soup
    dictionary_data = requests.get("https://www.spanishdict.com/translate/{}".format(word))
    soup = BeautifulSoup(dictionary_data.text, 'html.parser')

    trans = ""
    #get translation
    try:
      trans=split_word[1]
    except:
      all_trans = soup.select("a[class^=neodictTranslation]")
      for translation in all_trans:
        trans+="{}, ".format(translation.string)
      trans.strip(", ")
    #print(soup)
    sentences = soup.select('div[class^=indentSmall] div[class^=marginTopSmall]')

    s_sentence = ""
    e_sentence = ""
    for child in sentences:
      s_sentence = child.select_one('span[class^=exampleFirstHalf]').text
      e_sentence = child.select_one('span[class^=exampleSecondHalf]').text
      if(e_sentence != "" and len(e_sentence) > 2 and len(e_sentence) < 200):
        break

    return_object.append({
      "word":word,
      "pronunciation": "",
      "translation": trans,
      "t_sentence": s_sentence,
      "e_sentence": e_sentence,
      "level": "S",
    })
  return return_object

def get_cards_fra(all_words):
  return_object = []
  for word in all_words:
    print(word)
    if word == "":
      continue
    word = word.strip()
    split_word=word.split(',')
    word = split_word[0].strip()

    #Get soup
    dictionary_data = requests.get("https://www.linguee.com/english-french/search?source=auto&query={}".format(word))
    soup = BeautifulSoup(dictionary_data.text, 'html.parser')

    trans = ""
    #get translation
    try:
      trans=split_word[1]
    except:
      all_trans = soup.select("a.dictLink.featured")
      for translation in all_trans:
        if translation.string is not None:
          trans+="{}, ".format(translation.string)
      trans.strip(", ")

    sentences = soup.select('div.example_lines')

    f_sentence = ""
    e_sentence = ""
    for child in sentences:
      try:
        f_sentence = child.select_one('span.tag_s').text
        e_sentence = child.select_one('span.tag_t').text
      except:
        continue
      if(e_sentence != "" and len(e_sentence) > 2 and len(e_sentence) < 200):
        break

    return_object.append({
      "word":word,
      "pronunciation": "",
      "translation": trans,
      "t_sentence": f_sentence,
      "e_sentence": e_sentence,
      "level": "F",
    })

  return return_object

def get_chinese(all_words):
  return_object = []
  for word in all_words:
    print(word)
    if word == "":
      continue
    word = word.strip()
    split_word=word.split(',')
    word = split_word[0].strip()

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
    return_object.append({
      "word":word,
      "pronunciation": pinyin,
      "translation": trans,
      "t_sentence": c_sentence,
      "e_sentence": e_sentence,
      "level": "",
    })
  return return_object


@app.route('/playground')
def playground():
  return render_template('playground.html')



if __name__ == '__main__':
  app.run(debug=True)

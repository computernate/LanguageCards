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
def get_cards():
  return_object = []
  if request.method == "POST":
    all_words = request.get_json()
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
      hira = json.loads(hira_data.text)['converted']


      #Get translation
      level = 0
      try:
        trans=split_word[1]
      except:
        trans_data = requests.get("http://beta.jisho.org/api/v1/search/words?keyword={}".format(word))
        trans = ', '.join(json.loads(trans_data.text)['data'][0]['senses'][0]['english_definitions'])
        if len(json.loads(trans_data.text)['data'][0]['jlpt'])>0:
          level = json.loads(trans_data.text)['data'][0]['jlpt'][0][-1]


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
        print(sentence)
        print("https://jisho.org/search/{}%20%23sentences".format(word))

      if e_sentence=="": j_sentence=""

      return_object.append({
        "word":word,
        "hiragana": hira,
        "translation": trans,
        "j_sentence": j_sentence,
        "e_sentence": e_sentence,
        "level":level
      })

  return json.dumps(return_object)

if __name__ == '__main__':
  app.run(debug=True)

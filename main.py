from flask import Flask, render_template, request
import json

from cardcodes.japanese import get_cards_jap
from cardcodes.korean import get_korean_cards
from cardcodes.mandarin import get_chinese
from cardcodes.spanish import get_cards_esp
from db_functions import *
import os
from cardcodes.french import get_cards_fra

from tokenizers.french_tokenizer import tokenize as french_tokenize

#os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/home/n8ros/Documents/PERSONAL_PROJECT_TRANSLATIONS/google_api_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/var/www/html/LanguageCards/google_api_credentials.json"

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('card_create.html')

@app.route('/get_cards', methods=['POST'])
def get_cards_all():
  try:
    conn = create_db_connection()
    return_object = []
    return_object += get_cards_fra(request.get_json()['french'], conn)
    return_object += get_cards_esp(request.get_json()['spanish'], conn)
    return_object += get_cards_jap(request.get_json()['japanese'], conn)
    return_object += get_chinese(request.get_json()['chinese'], conn)
    return_object += get_korean_cards(request.get_json()['korean'], conn)
    conn.close()
    return json.dumps(return_object)
  except Exception as e:
    print(e)
    return json.dumps([{
        "language":"JP",
        "word":"",
        "pronunciation": str(e),
        "translation": "nateroskelley@gmail.com",
        "t_sentence": "Error message:",
        "e_sentence": "An error has occured. For help, please contact me at",
        "level": "Oh no!",
    }])


@app.route('/get_forms/2', methods=['POST'])
def get_french_tokenized():
  try:
    returnWords = []
    words = request.get_json()
    for word in words:
      try:
        returnWords.append(french_tokenize(word))
      except Exception as e:
        return {
            returnWords.append([{
                'BaseForm':"ERROR110",
                'Forms':[],
                'Language':-1,
                'Translations':""
            }])
        }
    print(returnWords)
    return json.dumps(returnWords)
  except Exception as e:
    print(e)
    return json.dumps({"ERROR:":str(e)})

@app.route('/playground')
def playground():
  return render_template('playground.html')

@app.route('/describe')
def describe_game():
    return render_template('describe.html', imageNames=json.dumps(os.listdir("D:\\nater\\Documents\\LanguageCards\\static\\images")))



if __name__ == '__main__':
  app.run()
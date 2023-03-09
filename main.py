from flask import Flask, render_template, request
import json

from cardcodes.japanese import get_cards_jap
from cardcodes.korean import get_korean_cards
from cardcodes.mandarin import get_chinese
from cardcodes.spanish import get_cards_esp
from db_functions import *
import os
from cardcodes.french import get_cards_fra
import random

from tokenizers.french_tokenizer import tokenize as french_tokenize

os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/home/n8ros/Documents/PERSONAL_PROJECT_TRANSLATIONS/google_api_credentials.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/var/www/html/LanguageCards/google_api_credentials.json"

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('card_create.html')

@app.route('/get_cards', methods=['POST'])
def get_cards_all():
  try:
    #conn = create_db_connection()
    conn = None
    return_object = []
    return_object += get_cards_fra(request.get_json()['french'], conn)
    return_object += get_cards_esp(request.get_json()['spanish'], conn)
    return_object += get_cards_jap(request.get_json()['japanese'], conn)
    return_object += get_chinese(request.get_json()['chinese'], conn)
    return_object += get_korean_cards(request.get_json()['korean'], conn)
    #conn.close()
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
    return render_template('describe.html', imageNames=json.dumps(os.listdir("/var/www/html/LanguageCards/static/images")))

@app.route('/situation/<id>/<user_id>')
def situation_game(id, user_id):
    return render_template('situation.html', id=id, user_id=user_id)

@app.route('/situation_home')
def situation_home():
    return render_template('situation_home.html')

@app.route('/sitaution_start')
def situation_start():
    return render_template('situation_start.html')

@app.route('/get_situation', methods=['GET'])
def get_situation():
    conn = create_db_connection()
    return json.dumps({
        'situation': get_situation_db(conn)[0][1],
        'condition': get_condition_db(conn)[0][1]
    })


@app.route('/new_situation', methods=['POST'])
def post_situation():
    if request.get_json()['type'] == "situation":
        add_situation(create_db_connection(), request.get_json()['data'])
    else:
        add_condition(create_db_connection(), request.get_json()['data'])
    return json.dumps({'status':'success'})

@app.route('/new_game', methods=['POST'])
def new_game():
    conn = create_db_connection()
    try:
        game_data = new_game_db(conn, request.get_json()['hostname'])
        return json.dumps(game_data)
    except Exception as e:
        return json.dumps({'error': '{}'.format(e)})

@app.route('/join_game', methods=['POST'])
def join_game():
    conn = create_db_connection()
    try:
        game_data = join_game_db(conn, request.get_json()['keycode'], request.get_json()['name'])
        return json.dumps(game_data)
    except Exception as e:
        return json.dumps({'error': '{}'.format(e)})

@app.route('/game_data/<id>', methods=['GET'])
def get_game_data(id):
    conn = create_db_connection()
    try:
        return json.dumps(game_data(conn, id))
    except Exception as e:
        return json.dumps({'error': '{}'.format(e)})

@app.route('/advance_game/<id>', methods=['GET'])
def advance_game(id):
    conn = create_db_connection()
    return json.dumps(update_game(conn, id))

@app.route('/remove_user/<id>', methods=['POST'])
def remove_user(id):
    conn = create_db_connection()
    try:
        remove_user_db(conn, id)
        return json.dumps({"Success":True})
    except Exception as e:
        return json.dumps({'error': '{}'.format(e)})

@app.route('/remove_situation/<id>', methods=['POST'])
def remove_situation(id):
    conn = create_db_connection()
    try:
        remove_situation_db(conn, id)
        return json.dumps({"Success":True})
    except Exception as e:
        return json.dumps({'error': '{}'.format(e)})

@app.route('/remove_condition/<id>', methods=['POST'])
def remove_condition(id):
    conn = create_db_connection()
    try:
        remove_condition_db(conn, id)
        return json.dumps({"Success": True})
    except Exception as e:
        return json.dumps({'error': '{}'.format(e)})
@app.route('/situation_mod')
def situation_mod():
    return render_template('situation_mod.html')

@app.route('/list_game_elements', methods=['POST'])
def list_game_elements():
    conn = create_db_connection()
    situations = list_situations(conn)
    conditions = list_conditions(conn)

    return {
        'situations':situations,
        'conditions':conditions
    }

@app.route('/add_point/<id>', methods=['POST'])
def add_point(id):
    conn = create_db_connection()
    add_point_db(conn, id)
    return {
        'success':True,
    }
@app.route('/remove_point/<id>', methods=['POST'])
def remove_point(id):
    conn = create_db_connection()
    remove_point_db(conn, id)
    return {
        'success':True,
    }

if __name__ == '__main__':
  app.run()
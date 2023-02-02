import string
import random

import mysql.connector


def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="tonguescards.ccyiqbgzjkvp.us-east-1.rds.amazonaws.com",
            user="tonguescards",
            password="3nT3R#cardsdb",
            database="tonguescards",
            port=3306
        )
    except mysql.connector.Error as err:
        print("Error: createdbconnection {}".format(err))
        print(err)

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        cursor.close()
        print("Error: execute_query {}".format(err))
        print(query)

def create_database():
  conn = create_db_connection()
  execute_query(conn, "CREATE TABLE cards (id INT AUTO_INCREMENT, language VARCHAR (8), word VARCHAR(64), pronunciation VARCHAR(64), translation VARCHAR(255), t_sentence VARCHAR(512), e_sentence VARCHAR(512), level VARCHAR (8), PRIMARY KEY(id));")

def create_situation_database():
  conn = create_db_connection()
  #execute_query(conn, "CREATE TABLE game_condition (id INT AUTO_INCREMENT, game_condition VARCHAR (255), likes INT(64), PRIMARY KEY(id));")
  #execute_query(conn,
  #  "CREATE TABLE players (id INT AUTO_INCREMENT, name VARCHAR(255), in_game INT(64), PRIMARY KEY(id));")
  #execute_query(conn,
  #                "CREATE TABLE games (id INT AUTO_INCREMENT, keycode VARCHAR (255), p1 INT(64), p2 INT(64), host INT(64), current_situation VARCHAR (255), current_condition VARCHAR (255), PRIMARY KEY(id));")



def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        cursor.close()
        print("ERROR: READ QUERY: {}".format(e))
        print(query)

def get_word(language, word, conn):
    return read_query(conn, f"SELECT * FROM cards WHERE language='{language}' AND word='{word}' LIMIT 1;")

def insert_word(conn, wo):
    execute_query(conn, f"INSERT INTO cards(language, word, pronunciation, translation, t_sentence, e_sentence, level) VALUES('{wo['language']}', '{wo['word']}', '{wo['pronunciation']}', '{wo['translation']}', '{wo['t_sentence']}', '{wo['e_sentence']}', '{wo['level']}');")

def add_situation(conn, sit):
    execute_query(conn, f"INSERT INTO situation(situation, likes) VALUES({repr(sit)}, 0);")
def add_condition(conn, cond):
    execute_query(conn, f"INSERT INTO game_condition(game_condition, likes) VALUES({repr(cond)}, 0);")
def get_situation_db(conn):
    return read_query(conn, f"SELECT * FROM situation ORDER BY RAND() LIMIT 1;")
def get_condition_db(conn):
    return read_query(conn, f"SELECT * FROM game_condition ORDER BY RAND() LIMIT 1;")
def get_player_db(conn, game):
    return read_query(conn, f"SELECT * FROM players WHERE in_game={game} ORDER BY RAND() LIMIT 1;")

def new_game_db(conn, hostname):
    execute_query(conn, f"INSERT INTO players (name, points) VALUES ('{hostname}', 0);")
    host = read_query(conn, f"SELECT id FROM players WHERE name = '{hostname}';")[0][0]
    key = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    execute_query(conn, f"INSERT INTO games (keycode, host, current_condition, current_situation) VALUES ('{key}', {host}, 'WAITING FOR HOST', 'WAITING FOR HOST');")
    game_id = read_query(conn, f"SELECT last_insert_id() from games;")[0][0]
    execute_query(conn, f"UPDATE players SET in_game={game_id} WHERE id={host};")
    return {
        'game_id':game_id,
        'user_id':host
    }

def join_game_db(conn, game, hostname):
    game_id = read_query(conn, f"SELECT id FROM games WHERE keycode={repr(game)}")[0][0]
    execute_query(conn, f"INSERT INTO players (name, in_game, points) VALUES ({repr(hostname)}, {game_id}, 0);")
    host = read_query(conn, f"SELECT id FROM players WHERE name = {repr(hostname)};")[0][0]
    return {
        'game_id':game_id,
        'user_id':host
    }

def update_game(conn, game):
    new_situation = get_situation_db(conn)[0][1]
    new_condition = get_condition_db(conn)[0][1]
    p1 = get_player_db(conn, game)[0][0]
    p2 = get_player_db(conn, game)[0][0]
    execute_query(conn, f"UPDATE games SET current_situation={repr(new_situation)}, current_condition={repr(new_condition)}, p1={repr(p1)}, p2={repr(p2)} WHERE id={game}")
    return 'success'

def game_data(conn, game_id):
    game = read_query(conn, f"SELECT * FROM games WHERE id={game_id}")[0]
    players = read_query(conn, f"SELECT * FROM players WHERE in_game={game_id}")
    return {
        'game':game,
        'players':players
    }

def remove_user_db(conn, id):
    print(F"REMOVING {id}")
    execute_query(conn, F"DELETE FROM players WHERE id={id}")
    is_host = read_query(conn, F"SELECT id FROM games WHERE host={id}")
    if len(is_host)!=0:
        print("HOST")
        execute_query(conn, F"DELETE FROM games WHERE id={is_host[0][0]}")
        execute_query(conn, F"DELETE FROM players WHERE in_game={is_host[0][0]}")

def remove_situation_db(conn, id):
    execute_query(conn, F"DELETE FROM situation WHERE id={id}")
def remove_condition_db(conn, id):
    execute_query(conn, F"DELETE FROM game_condition WHERE id={id}")
def list_situations(conn):
    return read_query(conn, "SELECT * FROM situation")
def list_conditions(conn):
    return read_query(conn, "SELECT * FROM game_condition")

def add_point_db(conn, id):
    execute_query(conn, F"UPDATE players SET points = points + 1 WHERE id = {id}")
def remove_point_db(conn, id):
    execute_query(conn, F"UPDATE players SET points = points - 1 WHERE id = {id}")

if __name__ == "__main__":
    conn = create_db_connection()
    rows = read_query(conn, "SELECT * FROM games")
    for row in rows:
        print(row)
    rows = read_query(conn, "SELECT * FROM players")
    for row in rows:
        print(row)
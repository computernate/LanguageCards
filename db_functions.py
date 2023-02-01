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
  execute_query(conn, "CREATE TABLE game_condition (id INT AUTO_INCREMENT, game_condition VARCHAR (255), likes INT(64), PRIMARY KEY(id));")


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
        print("ERROR: READ QUERY:" + e)
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

if __name__ == "__main__":
    create_situation_database()
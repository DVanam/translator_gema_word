import json
import sqlite3
import random
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

        self.words_list = []
        self.words_dict = dict()

    def create_table(self):
        """Создаем таблицу в базе данных для хранения данных."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS words
                                       (id INTEGER PRIMARY KEY,
                                       english TEXT,
                                       russian TEXT)''')
        self.connection.commit()

    def add_word_in_db(self, english, russian):
        """Добавление в таблицу базы даныз"""
        self.cursor.execute("INSERT INTO words (english, russian) VALUES (?, ?)", (english, russian))
        self.connection.commit()

    def save_to_json(self, filename):
        """Создание json file in database"""
        self.cursor.execute("SELECT * FROM words")
        words = self.cursor.fetchall()
        word_dict = [{"russian": row[1], "english": row[2]} for row in words]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(word_dict, f, indent=2)

    def load_from_json(self, filename):
        """Загрузка json file. Чере json.load."""
        with open(filename, "r") as f:
            word_dict = json.load(f)
            for i in range(len(word_dict)):
                ru = word_dict[i]["russian"]
                en = word_dict[i]["english"]
                # setdefault -Уникальных значений. Без повторов.
                self.words_dict.setdefault(ru, en)  # dict


    def get_table_db(self):
        # self.cursor.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT 1")
        self.cursor.execute("SELECT * FROM words")
        word_rand_db = self.cursor.fetchall()
        all_table_db = []
        for item in range(len(word_rand_db)):
            all_table_db.append(word_rand_db[item])
        return all_table_db

    def get_last_data(self):
        """Получаем последний сохраненный набор данных из базы данных."""
        self.cursor.execute("SELECT * FROM words ORDER BY id DESC LIMIT 1")
        rowd = self.cursor.fetchone()
        if rowd:
            return rowd[1], rowd[2]
        # return json.loads(result[0]) if result else []

    def __del__(self):
        """Close the database connection when the object is deleted."""
        self.connection.close()




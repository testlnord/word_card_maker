import psycopg2 as pg_driver
from werkzeug.security import safe_str_cmp
import hashlib
import user_methods


class DatabaseMethods:

    def __init__(self, db_user: str, db_password: str, db_host: str, db_name: str):
        self.db = pg_driver.connect(user=db_user, password=db_password, host=db_host, dbname=db_name)

    def insert_card(self, word: str, translation: str, context: str, deck: str):
        command: str = "INSERT INTO Card(word,translation,context,deck_id) VALUES('{}', '{}', '{}', " \
                       "(SELECT id FROM Deck WHERE name='{}'))".format(word, translation, context, deck)

        cur = self.db.cursor()
        try:
            cur.execute(command)
        finally:
            self.db.commit()
            cur.close()

    def add_deck(self, username: str, deck_name=None):

        if deck_name is None:
            deck_name = " ".join([username, "deck"])
        command: str = "INSERT INTO Deck(name, user_id) VALUES ('{}', (SELECT id FROM USERS WHERE login='{}'));".\
            format(deck_name, username)
        cur = self.db.cursor()
        try:
            cur.execute(command)
        finally:
            self.db.commit()
            cur.close()

    def add_user(self, username: str, password: str):
        command: str = "INSERT INTO Users(login, password_hash) VALUES ('{}', '{}');".\
            format(username, hashlib.sha512(password.encode('utf-8')).hexdigest())

        cur = self.db.cursor()
        try:
            cur.execute(command)
        finally:
            self.db.commit()
            cur.close()
        self.add_deck(username)
        self.__set_language(username, "en-ru")

    def __get_user(self, username) -> (str, str, str):

        command: str = "SELECT * FROM Users WHERE login='{}'".format(username)
        user_data = (None, None, None)
        cur = self.db.cursor()

        try:
            cur.execute(command)
            user_data = cur.fetchone()
        finally:
            self.db.commit()
            cur.close()
        return user_data

    def retrieve_user(self, username: str, password: str) -> user_methods.User:

        user_data = self.__get_user(username)

        if user_data is None:
            self.add_user(username, password)
            user_data = self.__get_user(username)

        if user_data and user_data[2] is None or safe_str_cmp(user_data[2],
                                                              hashlib.sha512(password.encode('utf-8')).hexdigest()):
            return user_methods.User(user_data[0], username, password)

        return None

    def retrieve_user_by_id(self, user_id) -> user_methods.User:
        command: str = "SELECT * FROM Users WHERE id='{}'".format(user_id)

        user_data = (None, None, None)
        cur = self.db.cursor()

        try:
            cur.execute(command)
            user_data = cur.fetchone()
        finally:
            self.db.commit()
            cur.close()

        if user_data:
            return user_methods.User(*user_data)

        return None

    def check_if_user_has_deck(self, user_id: str, deck_name: str) -> bool:
        has_rights = False
        command: str = "SELECT * FROM Deck WHERE name='{}' and user_id='{}'".format(deck_name, user_id)
        cur = self.db.cursor()

        try:
            cur.execute(command)
            if cur.fetchone():
                has_rights = True
        finally:
            self.db.commit()
            cur.close()
        return has_rights

    def __set_language(self, username: str, language: str):
        command: str = "INSERT INTO Settings(user_id, language) VALUES((SELECT id FROM Users WHERE login='{}'), '{}')"\
            .format(username, language)
        cur = self.db.cursor()

        try:
            cur.execute(command)
        finally:
            self.db.commit()
            cur.close()

    def set_language(self, username: str, language: str):
        command: str = "UPDATE Settings SET language = '{}' WHERE user_id=(SELECT id FROM Users WHERE login='{}')".\
            format(language, username)
        cur = self.db.cursor()

        try:
            cur.execute(command)
        finally:
            self.db.commit()
            cur.close()

    def get_language_by_id(self, user_id: str) -> str:
        command: str = "SELECT language FROM Settings WHERE user_id='{}'".format(user_id)
        lang = ""
        cur = self.db.cursor()

        try:
            cur.execute(command)
            lang = cur.fetchone()[0]
        finally:
            self.db.commit()
            cur.close()
        return lang

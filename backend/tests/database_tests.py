import unittest
from unittest import mock
import settings
from database import database_methods
import hashlib


class MyTestCase(unittest.TestCase):

    @mock.patch('psycopg2.connect')
    def test_insert_card(self, mock_con):
        methods = database_methods.DatabaseMethods(settings.DB_USER, settings.DB_PASSWORD,
                                                   "localhost", settings.DB_NAME)
        mock_db = mock_con.return_value
        mock_cur = mock_db.cursor.return_value
        methods.insert_card("test", "test", "test", 'Public deck')
        mock_db.cursor.assert_called_once()
        command: str = "INSERT INTO Card(word,translation,context,deck_id) VALUES('test', 'test', 'test', " \
                       "(SELECT id FROM Deck WHERE name='Public deck'))"
        mock_cur.execute.assert_called_with(command)

    @mock.patch('psycopg2.connect')
    def test_add_deck(self, mock_con):
        methods = database_methods.DatabaseMethods(settings.DB_USER, settings.DB_PASSWORD,
                                                   "localhost", settings.DB_NAME)
        mock_db = mock_con.return_value
        mock_cur = mock_db.cursor.return_value
        methods.add_deck("test")
        mock_db.cursor.assert_called_once()
        command: str = "INSERT INTO Deck(name, user_id) VALUES ('{}', (SELECT id FROM USERS WHERE login='{}'));".\
            format("test deck", "test")
        mock_cur.execute.assert_called_with(command)
        methods.add_deck("test", "deck 2")
        command: str = "INSERT INTO Deck(name, user_id) VALUES ('{}', (SELECT id FROM USERS WHERE login='{}'));". \
            format("deck 2", "test")
        mock_cur.execute.assert_called_with(command)

    @mock.patch('psycopg2.connect')
    def test_add_user(self, mock_con):
        methods = database_methods.DatabaseMethods(settings.DB_USER, settings.DB_PASSWORD,
                                                   "localhost", settings.DB_NAME)
        mock_db = mock_con.return_value
        mock_cur = mock_db.cursor.return_value
        methods.add_user("test", "test")
        mock_db.cursor.assert_called()
        command_user: str = "INSERT INTO Users(login, password_hash) VALUES ('{}', '{}');". \
            format("test", hashlib.sha512("test".encode('utf-8')).hexdigest())
        command_deck: str = "INSERT INTO Deck(name, user_id) VALUES ('{}', (SELECT id FROM USERS WHERE login='{}'));". \
            format("test deck", "test")
        command_lang: str = "INSERT INTO Settings(user_id, language) " \
                            "VALUES((SELECT id FROM Users WHERE login='{}'), '{}')".format("test", "en-ru")
        calls = [mock.call(command_user), mock.call(command_deck), mock.call(command_lang)]
        mock_cur.execute.assert_has_calls(calls)

    @mock.patch('user_methods.User')
    @mock.patch('psycopg2.connect')
    def test_retrieve_user_by_id(self, mock_con, mock_user):
        methods = database_methods.DatabaseMethods(settings.DB_USER, settings.DB_PASSWORD,
                                                   "localhost", settings.DB_NAME)
        mock_db = mock_con.return_value
        mock_cur = mock_db.cursor.return_value
        methods.retrieve_user_by_id("0")
        mock_db.cursor.assert_called_once()
        command = "SELECT * FROM Users WHERE id='{}'".format("0")
        mock_cur.execute.assert_called_with(command)

    @mock.patch('psycopg2.connect')
    def test_check_if_user_has_deck(self, mock_con):
        methods = database_methods.DatabaseMethods(settings.DB_USER, settings.DB_PASSWORD,
                                                   "localhost", settings.DB_NAME)
        mock_db = mock_con.return_value
        mock_cur = mock_db.cursor.return_value
        methods.check_if_user_has_deck("0", "test deck")
        mock_db.cursor.assert_called_once()
        command: str = "SELECT * FROM Deck WHERE name='{}' and user_id='{}'".format("test deck", "0")
        mock_cur.execute.assert_called_with(command)

    @mock.patch('psycopg2.connect')
    def test_set_language(self, mock_con):
        methods = database_methods.DatabaseMethods(settings.DB_USER, settings.DB_PASSWORD,
                                                   "localhost", settings.DB_NAME)
        mock_db = mock_con.return_value
        mock_cur = mock_db.cursor.return_value
        methods.set_language("test", "fr-ru")
        mock_db.cursor.assert_called_once()
        command: str = "UPDATE Settings SET language = '{}' WHERE user_id=(SELECT id FROM Users WHERE login='{}')".\
            format("fr-ru", "test")
        mock_cur.execute.assert_called_with(command)

    @mock.patch('psycopg2.connect')
    def test_get_language_by_id(self, mock_con):
        methods = database_methods.DatabaseMethods(settings.DB_USER, settings.DB_PASSWORD,
                                                   "localhost", settings.DB_NAME)
        mock_db = mock_con.return_value
        mock_cur = mock_db.cursor.return_value
        methods.get_language_by_id("0")
        mock_db.cursor.assert_called_once()
        command: str = "SELECT language FROM Settings WHERE user_id='{}'".format("0")
        mock_cur.execute.assert_called_with(command)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest import mock
import settings
from database import database_methods


class MyTestCase(unittest.TestCase):

    @mock.patch('psycopg2.connect')
    def test_insert(self, mock_con):
        methods = database_methods.DatabaseMethods(settings.DB_USER, settings.DB_PASSWORD,
                                                   "localhost", settings.DB_NAME)
        mock_db = mock_con.return_value
        mock_cur = mock_db.cursor.return_value
        methods.insert_card("test", "test", "test", 'Public deck')
        mock_db.cursor.assert_called_once()
        command: str = "INSERT INTO Card(word,translation,context,deck_id) VALUES('test', 'test', 'test', " \
                       "(SELECT id FROM Deck WHERE name='Public deck'))"
        mock_cur.execute.assert_called_with(command)

if __name__ == '__main__':
    unittest.main()

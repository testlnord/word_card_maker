import psycopg2 as pg_driver


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

import psycopg2 as pg_driver
import settings

db = pg_driver.connect(user=settings.DB_USER, password=settings.DB_PASSWORD, host="localhost", dbname=settings.DB_NAME)
cur = db.cursor()


def insert_card(word: str, translation: str, context: str, deck: str):
    command: str = "INSERT INTO Card(word,translation,context,deck_id) VALUES('{}', '{}', '{}', " \
                   "(SELECT id FROM Deck WHERE name='{}'))".format(word, translation, context, deck)
    cur.execute(command)
    db.commit()

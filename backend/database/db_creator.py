import psycopg2 as pg_driver


class DatabaseCreator:

    def __init__(self, db_user: str, db_password: str, db_host: str, db_name: str, db_port: int = 5432):
        self.db = pg_driver.connect(user=db_user, password=db_password, host=db_host, dbname=db_name, port=db_port)

    def create(self):
        with self.db.cursor() as cur:
            cur.execute(open("database/create.sql", "r").read())
            self.db.commit()

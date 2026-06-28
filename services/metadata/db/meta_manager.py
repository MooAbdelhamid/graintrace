import psycopg2
from db.config import config, get_connection_string
from psycopg2 import sql


class MetaDatabaseManager:
    def __init__(self):

        self._ensure_database()

        # self._init_tables()

        print("Database initialized")

    def _ensure_database(self):
        conn_params = get_connection_string("postgres")
        conn = psycopg2.connect(**conn_params)

        conn.autocommit = True

        cursor = conn.cursor()

        cursor.execute(
            """
                SELECT 1 FROM pg_database
                WHERE datname = %s
                """,
            (config.DB_NAME,),
        )

        exists = cursor.fetchone()
        if not exists:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config.DB_NAME))
            )

            print("Created central database")
        else:
            print("Central database exists")

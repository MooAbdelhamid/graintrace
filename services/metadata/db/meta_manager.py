import psycopg2
from db.config import config, get_connection_string
from db.table import add_row, create_meta_table, search_row
from psycopg2 import sql


class MetaDatabaseManager:
    def __init__(self):

        self._ensure_database()

        self._init_tables()

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

    def _init_tables(self):
        conn_params = get_connection_string(config.DB_NAME)
        conn = psycopg2.connect(**conn_params)

        cursor = conn.cursor()

        create_meta_table(cursor)

        conn.commit()

        print("Central database tables ready")

        cursor.close()
        conn.close()

    def store(self, bow_id, maker, bow_kind, owner):
        conn_params = get_connection_string(config.DB_NAME)
        conn = psycopg2.connect(**conn_params)

        cursor = conn.cursor()

        add_row(cursor, bow_id, maker, bow_kind, owner)

        conn.commit()
        cursor.close()
        conn.close()

    def search(self, bow_id):
        conn_params = get_connection_string(config.DB_NAME)
        conn = psycopg2.connect(**conn_params)

        cursor = conn.cursor()

        result = search_row(cursor, bow_id)

        conn.commit()
        cursor.close()
        conn.close()

        return result

    def delete(self):
        pass

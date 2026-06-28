def create_meta_table(cursor):
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    bow_id VARCHAR(100) PRIMARY KEY,
                    maker VARCHAR(255),
                    bow_kind VARCHAR(255),
                    owner VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            """)


def add_row(cursor, bow_id, maker, bow_kind, owner):
    cursor.execute(
        """
        INSERT INTO metadata (
            bow_id,
            maker,
            bow_kind,
            owner
        )
        VALUES (%s, %s, %s, %s)
        """,
        (bow_id, maker, bow_kind, owner),
    )


def search_row(cursor, bow_id):
    cursor.execute(
        """
        SELECT * 
        FROM metadata
        WHERE bow_id = %s
        """,
        (bow_id,),
    )
    return cursor.fetchone()

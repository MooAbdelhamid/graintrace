import psycopg2
from schemas.models import Bow

# from ..models import Bow


def create_meta_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            id VARCHAR(100) PRIMARY KEY,
            maker_assigned_id VARCHAR(255),
            certificate_no VARCHAR(255),
            stick_id_no VARCHAR(255),
            maker VARCHAR(255) NOT NULL,
            bow_kind VARCHAR(255),
            brand VARCHAR(255),
            school VARCHAR(255),
            owner VARCHAR(255),
            proof_created_by VARCHAR(255),
            place_of_issue VARCHAR(255),
            date_of_issue DATE,
            wood_registration_date DATE,
            import_proof VARCHAR(255),
            notes TEXT,
            materials JSONB,
            registered_at TIMESTAMP WITH TIME ZONE,
            updated_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            images BYTEA
        )
    """)


def add_row(cursor, bow: Bow, image_bytes: bytes):
    # Check if bow with id exists
    cursor.execute("SELECT 1 FROM metadata WHERE id = %s", (bow.id,))
    if cursor.fetchone():
        raise ValueError(f"Bow with id {bow.id} already exists")

    cursor.execute(
        # removed materials
        """
        INSERT INTO metadata (
            id, 
            maker_assigned_id, 
            certificate_no, 
            stick_id_no,
            maker, 
            bow_kind, 
            brand,
            school,
            owner, 
            proof_created_by,
            place_of_issue,
            date_of_issue,
            wood_registration_date,
            import_proof,
            notes, 
            registered_at, 
            updated_at, 
            images
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            bow.id,
            bow.maker_assigned_id,
            bow.certificate_no,
            bow.stick_id_no,
            bow.maker,
            bow.bow_kind,
            bow.brand,
            bow.school,
            bow.owner,
            bow.proof_created_by,
            bow.place_of_issue,
            bow.date_of_issue,
            bow.wood_registration_date,
            bow.import_proof,
            bow.notes,
            # json.dumps(bow.materials) if bow.materials else None,
            bow.registered_at,
            bow.updated_at,
            psycopg2.Binary(image_bytes) if image_bytes else None,
        ),
    )


def search_row(cursor, bow_id):
    cursor.execute(
        """
        SELECT * 
        FROM metadata 
        WHERE id = %s
        """,
        (bow_id,),
    )
    row = cursor.fetchone()
    if not row:
        return None
    colnames = [desc[0] for desc in cursor.description]
    result = dict(zip(colnames, row))

    # import json
    # if result.get("materials"):
    #     result["materials"] = json.loads(result["materials"])
    # materials = result.get("materials")
    # if materials and isinstance(materials, str):
    #    result["materials"] = json.loads(materials)

    return result


def delete_row(cursor, bow_id: str):
    cursor.execute(
        """
        DELETE FROM metadata
        WHERE id = %s
        """,
        (bow_id,),
    )
    if cursor.rowcount == 0:
        raise ValueError(f"Bow with id {bow_id} does not exist")


def delete_all_rows(cursor):
    cursor.execute("DELETE FROM metadata")


# def add_row(cursor, bow: Bow, image_bytes: bytes): # or list of bytes for multiple images?
#     cursor.execute(
#         """
#         INSERT INTO metadata (
#             id,
#             maker_assigned_id,
#             certificate_no,
#             stick_id_no,
#             maker,
#             bow_kind,
#             brand,
#             school,
#             owner,
#             proof_created_by,
#             place_of_issue,
#             date_of_issue,
#             wood_registration_date,
#             import_proof,
#             notes,
#             materials,
#             registered_at,
#             updated_at,
#             photos
#         )
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """,
#         (bow.id, bow.maker_assigned_id, bow.certificate_no, bow.stick_id_no, bow.maker, bow.bow_kind, bow.brand,
#          bow.school, bow.owner, bow.proof_created_by, bow.place_of_issue, bow.date_of_issue, bow.wood_registration_date,
#          bow.import_proof, bow.notes, bow.materials, bow.registered_at, bow.updated_at, psycopg2.Binary(image_bytes)),
#     )

# def search_row(cursor, bow_id):
#     cursor.execute(
#         """
#         SELECT *
#         FROM metadata
#         WHERE bow_id = %s
#         """,
#         (bow_id,),
#     )
#     return cursor.fetchone()

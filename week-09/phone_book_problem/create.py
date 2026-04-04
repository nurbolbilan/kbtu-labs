import psycopg2
from connect import get_connection

config = get_connection()

conn = get_connection()
with conn:
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE data
        (user_id SERIAL NOT NULL,
        user_name VARCHAR(50) NOT NULL,
        user_phone VARCHAR(15) NOT NULL,
        PRIMARY KEY (user_id, user_name)
        );
        """)
        conn.commit()


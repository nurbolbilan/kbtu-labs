import psycopg2
from config import load_config

config = load_config()

with psycopg2.connect(**config) as conn:
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE data
        (user_id SERIAL NOT NULL,
        user_name VARCHAR(50) NOT NULL,
        user_phone VARCHAR(15) NOT NULL,
        PRIMARY KEY (user_id, user_name)
        );
        """)
        conn.commit()


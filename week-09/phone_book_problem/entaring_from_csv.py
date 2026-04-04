import psycopg2
from config import load_config
from psycopg2.extras import execute_values


contacts = []
with open("csv.txt", "r", encoding="utf-8") as file:
    rows = file.readlines()
    for row in rows:
        contacts.append(row.strip().split(","))


config = load_config()
sql = """INSERT INTO data(user_name, user_phone)
         VALUES %s"""

with psycopg2.connect(**config) as conn:
    with conn.cursor() as cursor:
        execute_values(cursor, sql, contacts)


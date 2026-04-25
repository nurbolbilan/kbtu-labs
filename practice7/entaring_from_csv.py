from connect import get_connection
from psycopg2.extras import execute_values


contacts = []
with open("contacts.csv", "r", encoding="utf-8") as file:
    rows = file.readlines()
    for row in rows:
        contacts.append(row.strip().split(","))


sql = """INSERT INTO data(user_name, user_phone)
         VALUES %s"""

conn = get_connection()
with conn:
    with conn.cursor() as cursor:
        execute_values(cursor, sql, contacts)


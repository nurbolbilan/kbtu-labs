import psycopg2
from config import load_config

config = load_config()

sql = """INSERT INTO data(user_name, user_phone)
         VALUES(%s, %s) RETURNING user_id;"""

def insert(name, phone):
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, phone))
            conn.commit()

# while True:
#     answer = input("Continue? (y/n) ")
#     if answer == "n":
#         break
#     else:
#         name = input("Enter your name : ")
#         phone = input("Enter your phone number : ")
#         insert(name, phone)
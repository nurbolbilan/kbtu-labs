import psycopg2
from config import load_config

config = load_config()

def delete_by_name(user_name):
    sql = 'DELETE FROM data WHERE user_name = %s'
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (user_name,))
            conn.commit()

def delete_by_phone(user_phone):
    sql = 'DELETE FROM data WHERE user_phone = %s'
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (user_phone,))
            conn.commit()


# while True:
#     action = int(input("Enter action : (1. Delete by name \n 2. Delete by phone \n 3. Exit"))
#     if action == 1:
#         name = input("Enter name : ")
#         delete_by_name(name)
#     elif action == 2:
#         phone = input("Enter phone number : ")
#         delete_by_phone(phone)
#     elif action == 3:
#         break
#     else:
#         print("Invalid input")

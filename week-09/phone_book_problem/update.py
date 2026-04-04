import psycopg2
from config import load_config

config = load_config()

sql_for_name = """ UPDATE data
            SET user_name = %s
            WHERE user_id = %s"""

sql_for_phone = """ UPDATE data
            SET user_phone = %s
            WHERE user_id = %s"""

def update_for_name(name, user_id):
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_for_name, (name, user_id))
            conn.commit()

def update_for_phone(phone, user_id):
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_for_phone, (phone, user_id))
            conn.commit()

# while True:
#     answer1 = input("Do you want to update your data? (y/n) : ")
#     if answer1 == "n":
#         break
#     else:
#         answer2 = input("What do you want to update your data? (name/phone) : ")
#         if answer2 == "name":
#             user_id = input("Enter your user id : ")
#             name = input("Enter your name : ")
#             update_for_name(name, user_id)
#         elif answer2 == "phone":
#             user_id = input("Enter your user id : ")
#             phone = input("Enter your phone number : ")
#             update_for_phone(phone, user_id)
#         else:
#             print("Invalid input")
#             continue
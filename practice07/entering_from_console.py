from connect import get_connection

sql = """INSERT INTO data(user_name, user_phone)
         VALUES(%s, %s) RETURNING user_id;"""

def insert(name, phone):
    conn = get_connection()
    with conn:
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
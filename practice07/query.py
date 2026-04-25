from connect import get_connection

def all_name():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_name FROM data")
            return cur.fetchall()

def all_phone():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("select user_phone from data")
            return cur.fetchall()

def find_user_name(user_id):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("select user_id, user_name from data")
            rows = cur.fetchall()

            for row in rows:
                if row[0] == user_id:
                    return row[1]


def find_user_phone(user_id):
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("select user_id, user_phone from data")
            rows = cur.fetchall()

            for row in rows:
                if row[0] == user_id:
                    return row[1]

# while True:
#     action = input("Enter action: \n 1. output all phone \n 2. output all name \n 3. find user phone \n 4. find user name \n 5. exit \n")
#     if action == '1':
#         phone_list = all_phone()
#         for row in phone_list:
#             print(row)
#     elif action == '2':
#         name = all_name()
#         print(name)
#     elif action == '3':
#         user_id = int(input("Enter id : "))
#         name = find_user_name(user_id)
#         print(name)
#     elif action == '4':
#         user_id = int(input("Enter id : "))
#         phone = find_user_phone(user_id)
#         print(phone)
#     elif action == '5':
#         break
#     else:
#         print("Invalid input")


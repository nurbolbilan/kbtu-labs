from connect import get_connection

def first_task():
    cur.execute("SELECT returns_all_records();")
    user = cur.fetchall()
    for row in user:
        print(row[0])

def second_task(user_name, user_phone):
    cur.execute("CALL add_new_user(%s, %s);", (user_name, user_phone))
    conn.commit()

def third_task(names, phones):
    cur.execute("CALL add_many_new_users(%s, %s);", (names, phones))
    conn.commit()

def fourth_task():
    cur.execute("SELECT * FROM get_users_paged(%s, %s);", (5, 0))
    rows = cur.fetchall()
    for row in rows:
        print(row[0])

def fifth_task(user):
    cur.execute("CALL delete_users_data(%s);", (user,))
    conn.commit()

with get_connection() as conn:
    with conn.cursor() as cur:
        # second_task("Kazbek Kaz", "+77075656595")
        fourth_task()
import psycopg2
from connect import get_connection

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("CALL delete_users_data(%s);", ('Arnur Aibek',))
        conn.commit()

# cur.execute("SELECT returns_all_records();", (42,))
# user = cur.fetchall()
# for row in user:
#     print(row[0])

# cur.execute("CALL add_new_user(%s, %s);", ('Kazbek Tazbek', '77057869563'))
#         conn.commit()

# cur.execute("SELECT * FROM get_users_paged(%s, %s);", (5, 0))
#         rows = cur.fetchall()
#         for row in rows:
#             print(row[0])

# names = ['Arnur Aibek', 'Artur Aidos']
# phones = ['+77077648596', '+77077648546']
#
# cur.execute("CALL add_many_new_users(%s, %s);", (names, phones))
# conn.commit()
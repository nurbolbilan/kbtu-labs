import json, csv
from connect import conn

def fetch_contacts(group=None, email_query=None, sort_by="user_name", limit=5, offset=0):
    valid_sort = {"name": "c.user_name", "birthday": "c.birthday", "date_added": "c.user_id"}
    order = valid_sort.get(sort_by, "c.user_name")

    conditions = ["1=1"]
    params = []

    if group:
        conditions.append("g.group_name = %s")
        params.append(group)
    if email_query:
        conditions.append("c.email ILIKE %s")
        params.append(f"%{email_query}%")

    where = " AND ".join(conditions)
    sql = f"""
        SELECT c.user_id, c.user_name, c.email, c.birthday, g.group_name,
               STRING_AGG(p.phone || ' (' || p.phone_type || ')', ', ') AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.group_id
        LEFT JOIN phones p ON c.user_id  = p.contact_id
        WHERE {where}
        GROUP BY c.user_id, c.user_name, c.email, c.birthday, g.group_name
        ORDER BY {order}
        LIMIT %s OFFSET %s;
    """
    params += [limit, offset]

    with conn() as connection:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

def count_contacts(group=None, email_query=None):
    conditions = ["1=1"]
    params = []

    if group:
        conditions.append("g.group_name = %s")
        params.append(group)
    if email_query:
        conditions.append("c.email ILIKE %s")
        params.append(f"%{email_query}%")

    where = " AND ".join(conditions)
    sql = f"""
        SELECT COUNT(DISTINCT c.user_id)
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.group_id
        WHERE {where};
    """
    with conn() as connection:
        with connection.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()[0]

def print_results(rows, offset, limit, total):
    page = offset // limit + 1
    total_p = (total + limit - 1) // limit or 1

    print(f"\n{'─' * 60}")
    print(f"  Page {page} of {total_p}  |  Total contacts: {total}")
    print(f"{'─' * 60}")

    if not rows:
        print("  No contacts found.")
    else:
        for row in rows:
            uid, name, email, birthday, group, phones = row
            print(f"{uid} {name}")
            print(f"Phone: {phones or '—'}")
            print(f"Email: {email or '—'}")
            print(f"Birthday: {birthday or '—'}   Group: {group or '—'}")
            print()

    print(f"{'─' * 60}")

def pick_group():
    print("\nFilter by group:")
    groups = ["Family", "Work", "Friend", "Other"]
    for i, g in enumerate(groups, 1):
        print(f"  {i}. {g}")
    print("  0. No filter")

    choice = input("Choice: ").strip()
    if choice in ("1", "2", "3", "4"):
        return groups[int(choice) - 1]
    return None

def pick_sort():
    print("\nSort by:")
    print("  1. Name")
    print("  2. Birthday")
    print("  3. ID")
    choice = input("Choice: ").strip()
    return {"2": "birthday", "3": "date_added"}.get(choice, "name")

def add_phone():
    name  = input("Contact name: ").strip()
    phone = input("Phone number: ").strip()
    ptype = input("Type (mobile/work/home): ").strip() or "mobile"

    with conn() as connection:
        with connection.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        connection.commit()
    print(f"Phone added for '{name}'")

def move_to_group():
    name  = input("Contact name: ").strip()
    group = input("New group: ").strip()

    with conn() as connection:
        with connection.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
        connection.commit()
    print(f"'{name}' moved to group '{group}'")

def search_contacts():
    query = input("Search (name / email / phone): ").strip()

    with conn() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()

    print(f"\n{'─' * 60}")
    if not rows:
        print("  Nothing found.")
    else:
        for row in rows:
            uid, name, email, birthday, group, phones = row
            print(f"{uid} {name}")
            print(f"Phone: {phones or '—'}")
            print(f"Email: {email or '—'}")
            print(f"Birthday: {birthday or '—'}   Group: {group or '—'}")
            print()
    print(f"{'─' * 60}")

def export_json():
    sql = """
        SELECT c.user_id, c.user_name, c.email, c.birthday, g.group_name,
               STRING_AGG(p.phone || ' (' || p.phone_type || ')', ', ') AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.group_id
        LEFT JOIN phones p ON c.user_id  = p.contact_id
        GROUP BY c.user_id, c.user_name, c.email, c.birthday, g.group_name;
    """
    with conn() as connection:
        with connection.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()

    contacts = {}
    for row in result:
        contacts[row[0]] = {
            "name":     row[1],
            "email":    row[2],
            "birthday": str(row[3]),
            "group":    row[4],
            "phones":   row[5]
        }

    with open("contacts_export.json", "w") as f:
        json.dump(contacts, f, indent=4)

    print("Export done: contacts_export.json")

def import_json():
    with open("contacts_export.json", "r") as f:
        contacts = json.load(f)

    with conn() as connection:
        with connection.cursor() as cur:
            for _, data in contacts.items():

                cur.execute("SELECT user_id FROM contacts WHERE user_name = %s", (data["name"],))
                existing = cur.fetchone()

                if existing:
                    answer = input(f"Contact '{data['name']}' already exists. Overwrite? (y/n): ")
                    if answer.lower() != "y":
                        print(f"Skipping '{data['name']}'")
                        continue

                    cur.execute("""
                        UPDATE contacts SET email = %s, birthday = %s,
                        group_id = (SELECT group_id FROM groups WHERE group_name = %s)
                        WHERE user_name = %s
                    """, (data["email"], data["birthday"], data["group"], data["name"]))

                    contact_id = existing[0]
                    cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

                else:
                    cur.execute("SELECT group_id FROM groups WHERE group_name = %s", (data["group"],))
                    group = cur.fetchone()
                    if group:
                        group_id = group[0]
                    else:
                        cur.execute("INSERT INTO groups (group_name) VALUES (%s) RETURNING group_id", (data["group"],))
                        group_id = cur.fetchone()[0]

                    cur.execute("""
                        INSERT INTO contacts (user_name, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s) RETURNING user_id
                    """, (data["name"], data["email"], data["birthday"], group_id))
                    contact_id = cur.fetchone()[0]

                if data["phones"]:
                    for entry in data["phones"].split(", "):
                        entry = entry.strip()
                        if "(" in entry:
                            phone, ptype = entry.rstrip(")").split(" (")
                        else:
                            phone, ptype = entry, "mobile"
                        cur.execute("""
                            INSERT INTO phones (contact_id, phone, phone_type)
                            VALUES (%s, %s, %s)
                        """, (contact_id, phone.strip(), ptype.strip()))

        connection.commit()
    print("JSON import done")

def import_csv():
    with open("contacts.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        with conn() as connection:
            with connection.cursor() as cur:
                for row in reader:

                    cur.execute("SELECT group_id FROM groups WHERE group_name = %s", (row["group"],))
                    group = cur.fetchone()
                    if group:
                        group_id = group[0]
                    else:
                        cur.execute("INSERT INTO groups (group_name) VALUES (%s) RETURNING group_id", (row["group"],))
                        group_id = cur.fetchone()[0]

                    cur.execute("SELECT user_id FROM contacts WHERE user_name = %s", (row["name"],))
                    existing = cur.fetchone()

                    if existing:
                        answer = input(f"Contact '{row['name']}' already exists. Overwrite? (y/n): ")
                        if answer.lower() != "y":
                            print(f"Skipping '{row['name']}'")
                            continue

                        cur.execute("""
                            UPDATE contacts SET email = %s, birthday = %s, group_id = %s
                            WHERE user_id = %s
                        """, (row["email"], row["birthday"], group_id, existing[0]))

                        contact_id = existing[0]
                        cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

                    else:
                        cur.execute("""
                            INSERT INTO contacts (user_name, email, birthday, group_id)
                            VALUES (%s, %s, %s, %s) RETURNING user_id
                        """, (row["name"], row["email"], row["birthday"], group_id))
                        contact_id = cur.fetchone()[0]

                    if row.get("phone"):
                        cur.execute("""
                            INSERT INTO phones (contact_id, phone, phone_type)
                            VALUES (%s, %s, %s)
                        """, (contact_id, row["phone"], row.get("phone_type", "mobile")))

            connection.commit()
    print("CSV import done")

print("SEARCH AND FILTERING CONTACTS")
group = pick_group()
email_query = input("\nSearch by email (Enter to skip): ").strip() or None
sort_by = pick_sort()
limit = 3
offset = 0

while True:
    total = count_contacts(group=group, email_query=email_query)
    rows  = fetch_contacts(group=group, email_query=email_query,
                           sort_by=sort_by, limit=limit, offset=offset)
    print_results(rows, offset, limit, total)

    max_offset = ((total - 1) // limit) * limit if total else 0
    options = []
    if offset > 0:
        options.append("prev")
    if offset < max_offset:
        options.append("next")
    options += ["search", "add_phone", "move", "export", "import_json", "import_csv", "filter", "quit"]

    print("  Commands: " + " | ".join(options))
    cmd = input("  > ").strip().lower()

    if cmd == "next" and offset < max_offset:
        offset += limit
    elif cmd == "prev" and offset > 0:
        offset -= limit
    elif cmd == "search":
        search_contacts()
    elif cmd == "add_phone":
        add_phone()
    elif cmd == "move":
        move_to_group()
    elif cmd == "export":
        export_json()
    elif cmd == "import_json":
        import_json()
    elif cmd == "import_csv":
        import_csv()
    elif cmd == "filter":
        group = pick_group()
        email_query = input("\nSearch by email (Enter to skip): ").strip() or None
        sort_by = pick_sort()
        offset = 0
    elif cmd == "quit":
        print("\nGoodbye.")
        break
    else:
        print("  Unknown command, try again.")
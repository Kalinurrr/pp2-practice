import json
import csv
from connect import connect


def execute_sql_file(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()


def get_or_create_group(cur, group_name):
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group: ")
    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    conn = connect()
    cur = conn.cursor()

    group_id = get_or_create_group(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name) DO UPDATE
        SET email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        RETURNING id
        """,
        (name, email, birthday, group_id)
    )

    contact_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
        (contact_id, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact saved.")


def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT c.id, c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
        """
    )

    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Group name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        """,
        (f"%{group_name}%",)
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def search_by_email():
    email = input("Search email: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT name, email, birthday
        FROM contacts
        WHERE email ILIKE %s
        """,
        (f"%{email}%",)
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ")

    columns = {
        "1": "name",
        "2": "birthday",
        "3": "created_at"
    }

    column = columns.get(choice)

    if not column:
        print("Wrong choice.")
        return

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT name, email, birthday, created_at
        FROM contacts
        ORDER BY {column}
        """
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def search_all_fields():
    query = input("Search query: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def add_phone_to_contact():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type home/work/mobile: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added.")


def move_contact_to_group():
    name = input("Contact name: ")
    group = input("New group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved.")


def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
        """
    )

    contacts = []

    for row in cur.fetchall():
        contact_id, name, email, birthday, group_name, created_at = row

        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s",
            (contact_id,)
        )

        phones = [
            {"phone": p[0], "type": p[1]}
            for p in cur.fetchall()
        ]

        contacts.append({
            "name": name,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name,
            "created_at": str(created_at),
            "phones": phones
        })

    with open("contacts.json", "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Exported to contacts.json")


def import_json():
    with open("contacts.json", "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = connect()
    cur = conn.cursor()

    for contact in contacts:
        name = contact["name"]

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            action = input(f"{name} exists. skip/overwrite? ")

            if action.lower() == "skip":
                continue

            cur.execute("DELETE FROM contacts WHERE name = %s", (name,))

        group_id = get_or_create_group(cur, contact.get("group") or "Other")

        cur.execute(
            """
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (
                contact["name"],
                contact.get("email"),
                contact.get("birthday"),
                group_id
            )
        )

        contact_id = cur.fetchone()[0]

        for phone in contact.get("phones", []):
            cur.execute(
                """
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
                """,
                (
                    contact_id,
                    phone["phone"],
                    phone["type"]
                )
            )

    conn.commit()
    cur.close()
    conn.close()

    print("Imported from JSON.")


def import_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            group_id = get_or_create_group(cur, row["group"])

            cur.execute(
                """
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                SET email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
                """,
                (
                    row["name"],
                    row["email"],
                    row["birthday"],
                    group_id
                )
            )

            contact_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
                """,
                (
                    contact_id,
                    row["phone"],
                    row["phone_type"]
                )
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported.")


def paginated_console():
    page = 0
    limit = 5

    while True:
        offset = page * limit

        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT name, email, birthday, created_at
            FROM contacts
            ORDER BY id
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )

        rows = cur.fetchall()

        print(f"\nPage {page + 1}")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

        command = input("\nnext / prev / quit: ")

        if command == "next":
            page += 1
        elif command == "prev":
            if page > 0:
                page -= 1
        elif command == "quit":
            break
        else:
            print("Wrong command.")


def menu():
    while True:
        print("\nPHONEBOOK TSIS1")
        print("1. Add contact")
        print("2. Show contacts")
        print("3. Filter by group")
        print("4. Search by email")
        print("5. Sort contacts")
        print("6. Search all fields")
        print("7. Add phone")
        print("8. Move contact to group")
        print("9. Export JSON")
        print("10. Import JSON")
        print("11. Import CSV")
        print("12. Paginated navigation")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
          add_contact()
        elif choice == "2":
          show_contacts()
        elif choice == "3":
         filter_by_group()
        elif choice == "4":
         search_by_email()
        elif choice == "5":
         sort_contacts()
        elif choice == "6":
         search_all_fields()
        elif choice == "7":
         add_phone_to_contact()
        elif choice == "8":
         move_contact_to_group()
        elif choice == "9":
         export_json()
        elif choice == "10":
           import_json()
        elif choice == "11":
         import_csv()
        elif choice == "12":
         paginated_console()
        elif choice == "0":
         break
        else:
         print("Wrong choice.")
    



if __name__ == "__main__":
    execute_sql_file("schema.sql")
    execute_sql_file("procedures.sql")
    menu()
import os
import csv
from connect import connect


def insert_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added successfully!")


def get_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def update_contact(name, new_phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE contacts SET phone=%s WHERE name=%s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated successfully!")


def delete_contact(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name=%s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted successfully!")


def import_from_csv():
    conn = connect()
    cur = conn.cursor()

    file_path = os.path.join(os.path.dirname(__file__), "contacts.csv")

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Contacts imported successfully!")


while True:
    print("\n1. Add contact")
    print("2. Show contacts")
    print("3. Update contact")
    print("4. Delete contact")
    print("5. Exit")
    print("6. Import from CSV")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        insert_contact(name, phone)

    elif choice == "2":
        get_contacts()

    elif choice == "3":
        name = input("Name: ")
        phone = input("New phone: ")
        update_contact(name, phone)

    elif choice == "4":
        name = input("Name: ")
        delete_contact(name)

    elif choice == "5":
        print("Goodbye!")
        break

    elif choice == "6":
        import_from_csv()

    else:
        print("Invalid choice. Try again.")
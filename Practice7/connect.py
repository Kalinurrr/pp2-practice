import psycopg2

def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password="k12345r"
    )
    return conn
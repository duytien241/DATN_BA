import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_food_type(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM app_category")
    rows = cur.fetchall()
    return rows


def select_shop_in_location(conn, location):
    cur = conn.cursor()
    cur.execute("SELECT * FROM app_category")
    rows = cur.fetchall()
    return rows

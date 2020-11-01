import sqlite3


def create_connection():
    conn = None
    db_file = 'foodData/db.sqlite3'
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_test(conn):
    cur = conn.cursor()
    cur.execute("select name from app_menu limit(2)")
    rows = cur.fetchall()
    return rows


def select_shop_in_location(conn, location):
    cur = conn.cursor()
    cur.execute("SELECT * FROM app_category")
    rows = cur.fetchall()
    return rows


def get_shop_with_menu(conn, menu):
    cur = conn.cursor()
    cur.execute("""select app_restaurant.name from app_restaurant, app_menu
    where app_restaurant.id = app_menu.restaurant_id
    and app_menu.name like '{}'
    limit(5)""".format(menu))
    rows = cur.fetchall()
    return rows


def get_shop_with_name(conn, shop):
    cur = conn.cursor()
    cur.execute("""select name from app_restaurant
    where app_restaurant.name like '%{}%'
    limt(20)""".format(shop))
    rows = cur.fetchall()
    return rows


def get_location_of_shop(conn, shop):
    cur = conn.cursor()
    cur.execute("""select app_restaurant.name,app_restaurant.address,app_district.district from app_restaurant, app_district
    where app_restaurant.name like '%{}%'
    and app_restaurant.district_id = app_district.id
    limit(5)""".format(shop))
    rows = cur.fetchall()
    return rows


def get_time_of_shop(conn, shop):
    cur = conn.cursor()
    cur.execute("""select time_open from app_restaurant
    where app_restaurant.name like '%{}%'""".format(shop))
    rows = cur.fetchall()
    return rows


def get_time_of_shop_2(conn, shop):
    cur = conn.cursor()
    cur.execute("""select time_open from app_restaurant
    where app_restaurant.name like '%{}%'""".format(shop))
    rows = cur.fetchall()
    return rows

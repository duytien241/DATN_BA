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
    cur.execute("""select * from app_restaurant
    where app_restaurant.name like '%{}%'
    limit(20)""".format(shop))
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


def get_info_food(conn, item):
    cur = conn.cursor()
    cur.execute("""select app_restaurant.name,app_menu.price from app_menu, app_restaurant
    where app_restaurant.id = app_menu.restaurant and app_menu.name like '%{}%'""".format(item))
    rows = cur.fetchall()
    return rows


def get_shop_with_location(conn, item, loc):
    cur = conn.cursor()
    cur.execute("""select app_restaurant.name,app_restaurant.address,app_district.district from app_restaurant, app_district
    where app_restaurant.name like '%{}%'
    and app_district.district like '%{}%'
    and app_restaurant.district_id = app_district.id
    limit(5)
    """.format(item, loc))
    rows = cur.fetchall()
    return rows


def get_shop_food_with_location(conn, item, loc):
    cur = conn.cursor()
    cur.execute("""select app_restaurant.name,app_restaurant.address,app_district.district from app_restaurant, app_district, app_menu
    where app_menu.name like '%{}%'
    and app_district.district like '%{}%'
    and app_restaurant.district_id = app_district.id
    and app_restaurant.id = app_menu.restaurant_id
    limit(5)
    """.format(item, loc))
    rows = cur.fetchall()
    return rows


def get_food_with_name(conn, item, loc):
    cur = conn.cursor()
    cur.execute("""select app_restaurant.name,app_restaurant.address,app_district.district from app_restaurant, app_district
    where app_restaurant.name like '%{}%'
    and app_district.district like '%{}%'
    and app_restaurant.district_id = app_district.id
    limit(5)
    """.format(item, loc))
    rows = cur.fetchall()
    return rows

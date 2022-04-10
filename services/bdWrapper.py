import sqlite3
from config import *
from services.log import *

def check_user_presence(chat_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM users WHERE telegram_chat_id = '{chat_id}';")
    res = cur.fetchall()
    return len(res) == 1


def create_user(chat_id, username):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO users(telegram_chat_id, telegram_username) 
       VALUES('{chat_id}', '{username}');""")
    conn.commit()
    return True

def change_user_parametr(user_id, parametr_name, parametr_value):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""UPDATE users SET {parametr_name} = '{parametr_value}' WHERE telegram_chat_id = '{user_id}'""")
    conn.commit()
    return True

def get_all_users():
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users;")
    res = cur.fetchall()
    return res

def get_parameters():
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM settings;")
    res = cur.fetchall()
    return res

def get_texts():
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM texts;")
    res = cur.fetchall()
    return res

def get_parameter(parameter_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM settings WHERE id = {parameter_id};")
    res = cur.fetchone()
    return res



def get_setting(setting_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT value FROM settings WHERE id = '{setting_id}';")
    res = cur.fetchall()
    return res[0][0]


def set_setting(setting_id, setting_value):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""UPDATE settings SET value = '{setting_value}' WHERE id = '{setting_id}'""")
    conn.commit()
    return True


def get_text(setting_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT value FROM texts WHERE id = '{setting_id}';")
    res = cur.fetchall()
    return res[0][0]

def set_text(setting_id, value):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""UPDATE texts SET value = '{value}' WHERE id = '{setting_id}'""")
    conn.commit()
    return True

def get_all_categories():
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM categories;""")
    res = cur.fetchall()
    return res


def get_category_positions(category_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM products WHERE category_id = {category_id};""")
    res = cur.fetchall()
    return res

def get_position_by_id(product_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM products WHERE id = {product_id};""")
    res = cur.fetchone()
    return res

def get_category_by_id(category_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM categories WHERE id = {category_id};""")
    res = cur.fetchone()
    return res

def delcategory(category_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM categories WHERE id = {category_id};""")
    conn.commit()
    return True

def delproduct(product_id):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM products WHERE id = {product_id};""")
    conn.commit()
    return True

def addgood(category_id, name, description, price, photo):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO products(category_id, name, description, photo, price) 
       VALUES('{category_id}', '{name}', '{description}', '{photo}', {price});""")
    conn.commit()
    return True


def addcategory(name):
    conn = sqlite3.connect(BD_FILE_NAME)
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO categories(name) 
       VALUES('{name}');""")
    conn.commit()
    return True

import os
import pymysql
from dotenv import load_dotenv
import products
import couriers
import orders

products_list = []
couriers_list = []
orders_list = []


def database_connection():
    load_dotenv()
    host = os.environ.get("mysql_host")
    user = os.environ.get("mysql_user")
    password = os.environ.get("mysql_pass")
    database = os.environ.get("mysql_db")

    connection = pymysql.connect(
        host,
        user,
        password,
        database
    )
    return connection


def create_table():
    connection = database_connection()
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS `products` (
            `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(100) NOT NULL,
            `price` FLOAT NOT NULL
            )
        """)
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS `couriers` (
            `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(150) NOT NULL,
            `phone` VARCHAR(12) NOT NULL
            )
        """)
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS `orders` (
            `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `customer_name` VARCHAR(200) NOT NULL,
            `customer_address` VARCHAR(250) NOT NULL,
            `customer_phone` VARCHAR(15) NOT NULL,
            `courier` INT(100),
            `status` VARCHAR(100) NOT NULL,
            `items` VARCHAR(100)
            )
        """)
    connection.commit()
    
    load_products()
    load_couriers()
    load_orders()


def load_products():
    products_list.clear()
    connection = database_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM `products`')
        rows = cursor.fetchall()
        for row in rows:
            dictionary = {
                "id": row[0],
                "name": row[1],
                "price": row[2]
                }
            products_list.append(dictionary)
            connection.commit()
    except Exception as e:
        print(e)


def load_couriers():
    couriers_list.clear()
    connection = database_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM `couriers`')
        rows = cursor.fetchall()
        for row in rows:
            dictionary = {
                "id": row[0],
                "name": row[1],
                "phone": row[2]
                }
            couriers_list.append(dictionary)
            connection.commit()
    except Exception as e:
        print(e)


def load_orders():
    orders_list.clear()
    connection = database_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM `orders`')
        rows = cursor.fetchall()
        for row in rows:
            dictionary = {
                "id": row[0],
                "customer name": row[1],
                "customer address": row[2],
                "customer phone": row[3],
                "courier": row[4],
                "status": row[5],
                "items": row[6].split(", ")
                }
            orders_list.append(dictionary)
            connection.commit()
    except Exception as e:
        print(e)


def save_data():
    connection = database_connection()
    cursor = connection.cursor()
    cursor.close()
    connection.close()

    close_app()


def close_app():
    os.system('clear')
    print(
        "\nYour data has been saved. See you soon!\n\n"
        "      +   __            \n"
        "         / /  __ _____  .\n"
        "        / _ \/ // / -_) \n"
        "       /_.__/\_, /\__/   +\n"
        "            /___/       \n"
    )
    exit()


def error_message():
    print("\nCommand not recognized. Try again, please.")


def main_screen():
    os.system('clear')
    print(
        "       _\/_   __       ____\n"
        "        /\   / /  ___ / / /__  +\n"
        "            / _ \/ -_) / / _ \ \n"
        "     *     /_//_/\__/_/_/\___/  _\/_\n"
        "         +                       /\ \n"
        """
    Welcome to * Lunchapp * made by Simona.

        [0] save and exit the app
        [1] go to the product menu
        [2] go to the couriers menu
        [3] go to the orders menu"""
    )
    user_input = input(
        "\nTo navigate through the app, enter a number and press enter: ")
    if user_input == "0":
        save_data()
    elif user_input == "1":
        products.products_menu()
    elif user_input == "2":
        couriers.couriers_menu()
    elif user_input == "3":
        orders.orders_menu()
    else:
        input(
            "\nCommand not recognized, press any key to go to main menu.\n"
            )
        main_screen()


if __name__ == "__main__":
    create_table()
    while True:
        main_screen()

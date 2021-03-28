import pymysql
from dotenv import load_dotenv
import os
import app

products_sign = """                      __         __    
    ___  _______  ___/ /_ ______/ /____
   / _ \/ __/ _ \/ _  / // / __/ __(_-<
  / .__/_/  \___/\_,_/\_,_/\__/\__/___/
 /_/_________________________________/
    """


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


def choose_menu():
    user_input = input(
        "\nPress 0 to go to main menu or 1 to go back to products menu: "
        )
    if user_input == "0":
        app.main_screen()
    elif user_input == "1":
        products_menu()
    else:
        error_message()
        choose_menu()


def error_message():
    print(
        "\n   * Something went wrong, try again, please *"
        )


def products_menu():
    os.system('clear')
    print(products_sign)
    print(
        """    [0] return to the main screen
    [1] print all products
    [2] add a new product
    [3] update a product
    [4] delete a product"""
    )
    user_input = input()
    main_menu = user_input == "0"
    show = user_input == "1"
    add = user_input == "2"
    update = user_input == "3"
    remove = user_input == "4"

    if main_menu:
        app.main_screen()
    elif show:
        print_products_menu()
    elif add:
        add_product()
    elif update:
        update_product()
    elif remove:
        remove_product()
    else:
        error_message()
        choose_menu()


def print_products():
    app.load_products()
    connection = database_connection()
    cursor = connection.cursor()
    if len(app.products_list) == 0:
        print("   * There are no entries yet. *")
    else:
        try:
            cursor.execute('SELECT * FROM `products`')
            rows = cursor.fetchall()
            for row in rows:
                print(
                    f"   [{row[0]:2.0f}] {row[1]} / £{row[2]:.2f}"
                )
                connection.commit()
        except Exception as e:
            print(e)


def print_products_menu():
    os.system('clear')
    print(products_sign)
    print_products()
    choose_menu()


def add_product():
    os.system('clear')
    connection = database_connection()
    cursor = connection.cursor()
    print("   * You are adding a new product. *\n")
    product_name = input("Enter product's name: ")
    product_price = input("Enter the product's price: £")

    if not product_name or not product_price:
        error_message()
    elif product_name and product_price:
        try:
            cursor.execute(
                """INSERT INTO `products` (
                    `name`, `price`)
                    VALUES (%s, %s)""",
                (product_name, float(product_price))
                )
            connection.commit()
            print("\n   * You have successfully added a product. *")
        except Exception as e:
            print(e)
    choose_menu()


def choose_product():
    print_products()
    enter_number = input(
        "\nEnter the number of product (or 0 to cancel): ")
    if enter_number == "0":
        products_menu()
    elif enter_number:
        try:
            product_id = int(enter_number)
            for product in app.products_list:
                if ("id", product_id) in product.items():
                    return product_id
        except Exception as e:
            print(e)
            choose_menu()
    elif not enter_number:
        print("You haven't entered any number.")
        choose_menu()


def chosen_product(product_id):
    try:
        for product in app.products_list:
            for key, value in product.items():
                if product["id"] == product_id:
                    return product
    except Exception as e:
        print(e)


def update_product():
    os.system('clear')
    print("   * You are updating product info. *\n")
    product_id = choose_product()

    os.system('clear')
    product = chosen_product(product_id)
    name = product["name"]
    price = product["price"]

    print("   * You are updating product info. *\n")
    print(
        "Enter new data to overwrite, or leave blank to skip.\n")

    print("name: " + name)
    input_name = input()
    print("price: £" + str(price))
    input_price = input("£")

    if not input_name and not input_price:
        print("\n   * No data was changed. *")
    elif input_name or input_price:
        if input_name == "":
            pass
        else:
            update_name_in_database(product_id, input_name)

        if input_price == "":
            pass
        else:
            update_price_in_database(product_id, input_price)
        print("\n   * You have updated a product. *")
    choose_menu()


def update_name_in_database(product_id, updated_name):
    try:
        connection = database_connection()
        cursor = connection.cursor()
        cursor.execute("""UPDATE `products`
                    SET `name` = %s
                    WHERE `id` = %s""",
                    (updated_name, product_id))
        connection.commit()
    except Exception as e:
        print(e)


def update_price_in_database(product_id, updated_price):
    try:
        price = float(updated_price)
        connection = database_connection()
        cursor = connection.cursor()
        cursor.execute("""UPDATE `products`
                    SET `price` = %s
                    WHERE `id` = %s""",
                    (price, product_id))
        connection.commit()
    except Exception as e:
        print(e)


def remove_product():
    os.system('clear')
    print("   * You are removing a product. *\n")
    product_id = choose_product()
    try:
        connection = database_connection()
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM `products`
                    WHERE `id` = %s""",
                    (product_id))
        connection.commit()
        print("\n   * You have removed a product. *")
    except Exception as e:
        print(e)
    choose_menu()

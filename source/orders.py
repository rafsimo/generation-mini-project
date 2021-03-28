import os
import pymysql
from dotenv import load_dotenv
import app
import products
import couriers

orders_sign = """                  __          
     ___  _______/ /__ _______
    / _ \/ __/ _  / -_) __(_-<
    \___/_/  \_,_/\__/_/ /___/
     \______________________/
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
        "\nPress 0 to go to main menu or 1 to go back to orders menu: "
        )
    if user_input == "0":
        app.main_screen()
    elif user_input == "1":
        orders_menu()
    else:
        error_message()
        choose_menu()


def error_message():
    print(
        "\n   * Something went wrong, try again, please *"
        )


def orders_menu():
    os.system('clear')
    print(orders_sign)
    print(
        """    [0] return to the main screen
    [1] print all orders
    [2] create new order
    [3] update order status
    [4] update order
    [5] remove order"""
    )
    user_input = input()
    main_menu = user_input == "0"
    show = user_input == "1"
    add = user_input == "2"
    update_status = user_input == "3"
    update_order = user_input == "4"
    remove = user_input == "5"

    if main_menu:
        app.main_screen()
    elif show:
        print_orders_menu()
    elif add:
        create_order()
    elif update_status:
        update_order_status()
    elif update_order:
        update_order_data()
    elif remove:
        remove_order()
    else:
        error_message()
        choose_menu()


def print_orders():
    app.load_orders()
    if len(app.orders_list) != 0:
        for order in app.orders_list:
            order_id = order["id"]
            name = order["customer name"]
            address = order["customer address"]
            phone = order["customer phone"]
            courier = order["courier"]
            status = order["status"]
            items = order["items"]
            print(f"""   [{order_id:2.0f}] customer name: {name}
        customer address: {address}
        customer phone: {phone}
        courier: {courier}
        status: {status}
        items: {items}
        """)
    else:
        print("   * There is no data yet! *")


def print_orders_menu():
    os.system('clear')
    print(orders_sign)
    print_orders()
    choose_menu()


def create_order():
    os.system('clear')
    print("   * You are adding a new order. *\n")
    input_name = input("Enter customer's name: ")
    input_address = input("Enter customer's addres: ")
    input_phone = input("Enter customer's phone number: +44")
    if not input_name or not input_address or not input_phone:
        error_message()
    elif input_name and input_address and input_phone:
        new_order = {
            "name": input_name.title(),
            "address": input_address,
            "phone": input_phone,
            "courier": None,
            "status": "preparing order",
            "items": None
        }
        add_products(new_order)
        assign_courier(new_order)
        add_order_to_database(new_order)
        print("\n   * You have successfully added a new order. *")
    choose_menu()


def assign_courier(order):
    os.system('clear')
    print("\n   * You are assigning courier to the order. *\n")
    couriers.print_couriers()
    try:
        courier_number = input(
            "\nEnter the number of courier to assign to the order: ")
        if courier_number:
            order["courier"] = int(courier_number)
        elif not courier_number:
            print("   * No courier was assigned. *")
    except Exception as e:
        print(e)
        choose_menu()


def add_products(order):
    os.system('clear')
    app.load_products()
    print("\n   * You are adding products to the order. *\n")
    products.print_products()
    print("\nYou can add multiple products as many times as you like.")

    while True:
        order_input = input(
            "Enter one product number at the time (or 0 when you are done): "
        )
        if order_input != "0":
            try:
                if order["items"] is None:
                    order["items"] = order_input
                else:
                    order["items"] += ", " + order_input
                continue
            except Exception as e:
                print(e)
                continue
        elif order_input == "0":
            break


def add_order_to_database(order):
    connection = database_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """INSERT INTO `orders` (
                `customer_name`,
                `customer_address`,
                `customer_phone`,
                `courier`,
                `status`,
                `items`
                )
                VALUES (%s, %s, %s, %s, %s, %s)""", (
                    order["name"],
                    order["address"],
                    order["phone"],
                    order["courier"],
                    order["status"],
                    order["items"]
                    )
        )
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        choose_menu()


def choose_order():
    print_orders()
    enter_number = input(
        "\nEnter the number of order to update (or 0 to cancel): ")
    if enter_number == "0":
        orders_menu()
    elif enter_number:
        try:
            order_id = int(enter_number)
            for order in app.orders_list:
                if ("id", order_id) in order.items():
                    return order_id
        except Exception as e:
            print(e)
            choose_menu()
    elif not enter_number:
        print("\n   * You haven't entered any number. *")
        choose_menu()


def chosen_order(order_id):
    try:
        for order in app.orders_list:
            for key, value in order.items():
                if order["id"] == order_id:
                    return order
    except Exception as e:
        print(e)


def update_order_status():
    os.system('clear')
    print("\n   * You are changing order's status. *\n")
    order_id = choose_order()

    os.system('clear')
    print("   * You are updating this order's status: *\n")
    for key, value in chosen_order(order_id).items():
        print(f"    {key}: {value}")
    user_input = input(
        """\nOptions:\n
    [0] order cancelled
    [1] preparing order
    [2] delivering order
    [3] order finished
        """
        "\nEnter a number to change status of the order: "
        )
    cancelled = user_input == "0"
    preparing = user_input == "1"
    delivering = user_input == "2"
    finished = user_input == "3"
    try:
        if user_input:
            if cancelled:
                update_order_status_in_database(
                    order_id, "order canceled")
            elif preparing:
                update_order_status_in_database(
                    order_id, "preparing order")
            elif delivering:
                update_order_status_in_database(
                    order_id, "delivering order")
            elif finished:
                update_order_status_in_database(
                    order_id, "order finished")
            print("\n   * Order has been successfully updated. *")
    except Exception as e:
        print(e)
    choose_menu()


def update_order_status_in_database(order_id, new_status):
    connection = database_connection()
    cursor = connection.cursor()
    cursor.execute("""UPDATE `orders`
        SET `status` = %s
        WHERE `id` = %s
        """,
        (new_status, order_id)
        )
    connection.commit()


def update_order_data():
    os.system('clear')
    print("   * You are updating order info. *\n")
    if len(app.orders_list) != 0:
        id_order = choose_order()
    else:
        print("   * There is no order to update. *")
        choose_menu()

    os.system('clear')
    order = chosen_order(id_order)

    name = order["customer name"]
    address = order["customer address"]
    phone = order["customer phone"]
    courier = order["courier"]

    print("   * You are updating order info. *\n")
    print(
        "Enter new data to overwrite, or leave blank to skip.\n")

    print("customer name: " + name)
    input_name = input()
    print("customer address: " + address)
    input_address = input()
    print("customer phone: (+44)" + phone)
    input_phone = input("(+44)")

    update_name_in_database(id_order, input_name)
    update_address_in_database(id_order, input_address)
    update_phone_in_database(id_order, input_phone)

    print("\ncourier: " + str(courier))
    input_courier = input(
        "Press 1 to assign a different courier (otherwise leave empty): ")
    if input_courier == "":
        pass
    elif input_courier == "1":
        change_courier(id_order)

    print("\nitems: " + ", ".join(order["items"]))
    input_items = input(
        "Press 1 to change items (otherwise leave empty): ")
    if input_items == "":
        pass
    elif input_items == "1":
        change_products(id_order)

    print("\n   * You have successfully updated the order. *")
    choose_menu()


def update_name_in_database(order_id, updated_name):
    try:
        if updated_name == "":
            pass
        else:
            connection = database_connection()
            cursor = connection.cursor()
            cursor.execute("""UPDATE `orders`
                        SET `customer_name` = %s
                        WHERE `id` = %s""",
                            (updated_name,
                            order_id)
                        )
            connection.commit()
    except Exception as e:
        print(e)


def update_address_in_database(order_id, updated_address):
    if updated_address == "":
        pass
    else:
        try:
            connection = database_connection()
            cursor = connection.cursor()
            cursor.execute("""UPDATE `orders`
                        SET `customer_address` = %s
                        WHERE `id` = %s""",
                        (updated_address, order_id))
            connection.commit()
        except Exception as e:
            print(e)


def update_phone_in_database(order_id, updated_phone):
    if updated_phone == "":
        pass
    else:
        try:
            connection = database_connection()
            cursor = connection.cursor()
            cursor.execute("""UPDATE `orders`
                        SET `customer_phone` = %s
                        WHERE `id` = %s""",
                        (updated_phone, order_id))
            connection.commit()
        except Exception as e:
            print(e)


def change_courier(order_id):
    os.system('clear')
    print("\n   * You are assigning courier to the order. *\n")
    couriers.print_couriers()
    try:
        courier_number = input(
            "\nEnter the number of courier to assign to the order: ")
        if int(courier_number):
            connection = database_connection()
            cursor = connection.cursor()
            cursor.execute("""UPDATE `orders`
                        SET `courier` = %s
                        WHERE `id` = %s""",
                        (courier_number, order_id))
            connection.commit()
        elif not courier_number:
            print("   * No courier was assigned. *")
    except Exception as e:
        print(e)
        choose_menu()


def change_products(order_id):
    os.system('clear')
    app.load_products()
    print("\n   * You are adding products to the order. *\n")
    products.print_products()
    print("\nYou can add multiple products as many times as you like.")
    new_products = None
    while True:
        order_input = input(
        "Enter one product number at the time (or 0 when you are done): "
        )
        try:
            if order_input != "0":
                if new_products is None:
                    new_products = order_input
                    continue
                else:
                    new_products += ", " + order_input
                    continue
            elif order_input == "0":
                break
                connection = database_connection()
                cursor = connection.cursor()
                cursor.execute("""UPDATE `orders`
                            SET `items` = %s
                            WHERE `id` = %s""",
                            (new_products, order_id))
                connection.commit()
        except Exception as e:
            print(e)
            continue


def remove_order():
    os.system('clear')
    print("   * You are removing an order. *\n")
    order_id = choose_order()
    try:
        connection = database_connection()
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM `orders`
                    WHERE `id` = %s""",
                    (order_id))
        connection.commit()
        print("\n   * You have removed a order. *")
    except Exception as e:
        print(e)
    choose_menu()
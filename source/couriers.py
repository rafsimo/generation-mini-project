import pymysql
from dotenv import load_dotenv
import os
import app

couriers_sign = """                        _           
     _______  __ ______(_)__ _______
    / __/ _ \/ // / __/ / -_) __(_-< 
    \__/\___/\_,_/_/ /_/\__/_/ /___/  
     \____________________________/
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
        "\nPress 0 to go to main menu or 1 to go back to couriers menu: "
        )
    if user_input == "0":
        app.main_screen()
    elif user_input == "1":
        couriers_menu()
    else:
        error_message()
        choose_menu()


def error_message():
    print(
        "\n   * Something went wrong, try again, please *"
        )


def couriers_menu():
    os.system('clear')
    print(couriers_sign)
    print(
        """    [0] return to the main screen
    [1] print all couriers
    [2] add a new courier
    [3] update a courier
    [4] delete a courier"""
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
        print_couriers_menu()
    elif add:
        add_courier()
    elif update:
        update_courier()
    elif remove:
        remove_courier()
    else:
        error_message()
        choose_menu()


def print_couriers():
    app.load_couriers()
    connection = database_connection()
    cursor = connection.cursor()
    if len(app.couriers_list) == 0:
        print("   * There are no entries yet. *")
    else:
        try:
            cursor.execute('SELECT * FROM `couriers`')
            rows = cursor.fetchall()
            for row in rows:
                print(
                    f"   [{row[0]:2.0f}] {row[1]} / (+44){row[2]}"
                )
                connection.commit()
        except Exception as e:
            print(e)


def print_couriers_menu():
    os.system('clear')
    print(couriers_sign)
    print_couriers()
    choose_menu()


def add_courier():
    os.system('clear')
    connection = database_connection()
    cursor = connection.cursor()
    print("   * You are adding a new courier. *\n")
    courier_name = input("Enter courier's name: ")
    courier_phone = input("Enter courier's phone number: +44")

    if not courier_name or not courier_phone:
        error_message()
    elif courier_name and courier_phone:
        try:
            cursor.execute(
                """INSERT INTO `couriers` (
                    `name`, `phone` )
                    VALUES (%s, %s)""",
                (courier_name, courier_phone))
            connection.commit()
            print("\n   * You have successfully added a courier. *")
            choose_menu()
        except Exception as e:
            print(e)
    choose_menu()


def choose_courier():
    print_couriers()
    enter_number = input(
        "\nEnter the number of courier (or 0 to cancel): ")
    if enter_number == "0":
        couriers_menu()
    elif enter_number:
        try:
            courier_id = int(enter_number)
            for courier in app.couriers_list:
                if ("id", courier_id) in courier.items():
                    return courier_id
        except Exception as e:
            print(e)
            choose_menu()
    elif not enter_number:
        print("You haven't entered any number.")
        choose_menu()


def chosen_courier(courier_id):
    try:
        for courier in app.couriers_list:
            for key, value in courier.items():
                if courier["id"] == courier_id:
                    return courier
    except Exception as e:
        print(e)


def update_courier():
    os.system('clear')
    print("   * You are updating courier info. *\n")
    courier_id = choose_courier()
    os.system('clear')
    courier = chosen_courier(courier_id)
    name = courier["name"]
    phone = courier["phone"]
    print("   * You are updating courier info. *\n")
    print(
        "Enter new data to overwrite, or leave blank to skip.\n")
    print("name: " + name)
    input_name = input()
    print("phone: (+44)" + str(phone))
    input_phone = input("(+44)")

    if not input_name and not input_phone:
        print("\n   * No data was changed. *")
    elif input_name or input_phone:
        # updates info in database if it's not empty
        update_name_in_database(courier_id, input_name)
        update_phone_in_database(courier_id, input_phone)
        print("\n   * You have updated a courier. *")
    choose_menu()


def update_name_in_database(courier_id, updated_name):
    if updated_name == "":
        pass
    else:
        try:
            connection = database_connection()
            cursor = connection.cursor()
            cursor.execute("""UPDATE `couriers`
                        SET `name` = %s
                        WHERE `id` = %s""",
                        (updated_name, courier_id))
            connection.commit()
        except Exception as e:
            print(e)


def update_phone_in_database(courier_id, updated_phone):
    if updated_phone == "":
        pass
    else:
        try:
            phone = float(updated_phone)
            connection = database_connection()
            cursor = connection.cursor()
            cursor.execute("""UPDATE `couriers`
                        SET `phone` = %s
                        WHERE `id` = %s""",
                        (phone, courier_id))
            connection.commit()
        except Exception as e:
            print(e)


def remove_courier():
    os.system('clear')
    print("   * You are removing a courier. *\n")
    courier_id = choose_courier()
    try:
        connection = database_connection()
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM `couriers`
                    WHERE `id` = %s""",
                    (courier_id))
        connection.commit()
        print("\n   * You have removed a courier. *")
    except Exception as e:
        print(e)
    choose_menu()

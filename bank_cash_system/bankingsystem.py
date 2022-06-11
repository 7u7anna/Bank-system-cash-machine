# sql connector

from argparse import _MutuallyExclusiveGroup
from multiprocessing.sharedctypes import Value
from sre_compile import isstring
from sys import excepthook
import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='sqluser',
    password='1234',
    database='cashsystem'
)
mycursor = mydb.cursor()

# python oop code

class User():

    def __init__(self, name, acc_numb, pin, password):
        self.name = name
        self.acc_numb = acc_numb
        self.pin = pin
        self.password = password


class System(User):

    def __init__(self, name, acc_numb, pin, password, balance):
        super().__init__(name, acc_numb, pin, password)
        self.balance = balance

    def show_details(self):
        print(f"{active_u.name} your current balance is {active_u.balance}")

    def deposit(self):
        am = int(input('How much money would you like to deposit? '))
        mycursor.execute(
            "SELECT balance FROM users WHERE login = %s", (active_u.acc_numb, )
        )
        active_u.balance = mycursor.fetchone()[0]
        active_u.balance += am
        mycursor.execute(
            "UPDATE users SET balance = %s WHERE login = %s", (
                active_u.balance, active_u.acc_numb, )
        )
        print(
            f"Thank you for using our bank. Account {active_u.acc_numb} current balance is {active_u.balance}")

    def withdrawl(self):
        am = int(input('How much money would you like to withdrawl? '))
        mycursor.execute(
            "SELECT balance FROM users WHERE login = %s", (active_u.acc_numb, )
        )
        active_u.balance = mycursor.fetchone()[0]
        if am > active_u.balance or am <= 0:
            print(f"Transaction rejected")
        else:
            active_u.balance -= am
            mycursor.execute(
                "UPDATE users SET balance = %s WHERE login = %s", (
                    active_u.balance, active_u.acc_numb, )
            )
            print(
                f"Thank you using our bank. {active_u.acc_numb} current balance is {active_u.balance}")

    def unblock(self):

        # check account status

        mycursor.execute(
            "SELECT blocked FROM users WHERE login = %s", (active_u.acc_numb, )
        )
        get_data = mycursor.fetchone()[0]
        if get_data == 'False':
            print(f"Account {active_u.acc_numb} is already unblocked")
        else:
            print(
                f"'Are you sure to unblock {active_u.acc_numb} account? 1) yes 2) No'")
            to_unblock = int(input())
            while to_unblock != 1 and to_unblock != 2:
                to_unblock = int(input('Please choose option 1 or 2'))
            if to_unblock == 1:
                mycursor.execute(
                    "SELECT password FROM users WHERE login = %s", (
                        active_u.acc_numb, )
                )
                get_password_from_db = mycursor.fetchone()[0]
                authorize = str(input('Please enter auxility password'))
                if authorize == get_password_from_db:

                    # update blocked data in the database

                    mycursor.execute(
                        "UPDATE users SET blocked = 'False' WHERE login = %s", (
                            active_u.acc_numb, )
                    )
                    print(f"Account {active_u.login} successfully ublocked")
                else:
                    print(
                        f"Incorrect password. We could not unblock {active_u.acc_numb} account. Try again later")
            elif to_unblock == 2:
                print(f"Account {active_u.acc_numb} is still blocked")

# call algorithm


while True:
    print()
    print(f"Choose option")
    print(f"1) I have account 2) I want to register ")
    if_client = int(input())
    while if_client == None:
        if_client == int(input('Please choose option '))
    while if_client != 1 and if_client != 2:
        if_client = int(input('Please choose option 1 or 2 '))
    if if_client == 1:

        # Choose option from available

        print('Welcome in XXX Bank')
        print(f"Choose option")
        print(f"1) Show current balance\n2) Withdrawl money\n3) Deposit money\n4) Unblock account")

    # check if user input is number

        while True:
            try:
                user_option = int(input())
                break
            except ValueError:
                print('Invalid option. Try again ')

    # authorize existing user from database
    # get login from users table based on client input
        if user_option == 1 or user_option == 2 or user_option == 3 or user_option == 4:
            enter_login = input('Enter login ')
            mycursor.execute(
                "SELECT login FROM users WHERE login = %s;", (enter_login, )
            )
            get_login_from_db = mycursor.fetchone()
            if get_login_from_db == None:
                print(f"Account does not exist")
            else:

                # get pin from users table based on input existing login

                mycursor.execute(
                    "SELECT pin FROM users WHERE login = %s;", (enter_login, )
                )
                get_pin_from_db = mycursor.fetchone()[0]
                enter_pin = input('Enter pin ')

            # check if input pin is correct/authorization
                tries = 1
                while enter_pin != get_pin_from_db:
                    enter_pin = input(f"Incorrect pin. Try again ")
                    tries += 1
                    if tries == 3:
                        print(
                            f"Account {enter_login} is blocked to unblock please choose 'unblock account' in menu ")
                        mycursor.execute(
                            "UPDATE users SET blocked = 'True' WHERE login = %s", (
                                enter_login, )
                        )
                        print(f"Thank you for choosing XXX Bank")
                        break

                # actions after pin correct

                if enter_pin == get_pin_from_db:
                    print(f"Correct pin")
                    mycursor.execute(
                        "SELECT name, login, pin, password, balance FROM users WHERE login = %s;", (
                            enter_login, )
                    )
                    get_user_data = mycursor.fetchone()

                # read data from the table

                    name = get_user_data[0]
                    login = get_user_data[1]
                    pin = get_user_data[2]
                    password = get_user_data[3]
                    balance = get_user_data[4]
                    active_u = System(name, login, pin, password, balance)

                # redirect user to the function based on client choice

                    if user_option == 1:
                        active_u.show_details()
                    elif user_option == 2:
                        active_u.withdrawl()
                    elif user_option == 3:
                        active_u.deposit()
                    elif user_option == 4:
                        active_u.unblock()

    # create new user account in database

    elif if_client == 2:
        print(f"You need to fill your data form")
        name = str(input('name: '))
        login = str(input('login: '))
        pin = int(input('4-digit pin number: '))
        while len(str(pin)) != 4:
            pin = int(input('Pin code does not match criteria. Try again '))
        password = str(input('password (10-character): '))
        while len(str(password)) >= 10:
            password = str(
                input('Password does not match criteria. Try again '))
        balance = 0
        mycursor.execute(
            "INSERT INTO users(name, login, pin, password, balance) VALUES (%s, %s, %s, %s, %s)",
            (name, login, pin, password, balance)
        )
        print(f'Account registered. Thank you for choosing XXX Bank')

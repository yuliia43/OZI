import re
import colorama
from colorama import Fore, Style
from users_structure import *
from computer_info_searcher import *


class Program_menu():

    def __init__(self):
        self.exit_menu = False
        self.current_state = "MAIN"
        self.users = UsersStructure()

    def show_menu(self):
        if self.current_state == "MAIN":
            print("_____________________\nMAIN MENU\n_____________________\n"
                  "0. Exit\n"
                  "1. About\n"
                  "2. Authorize")
            chose = input()
            self.main_menu(chose)
        elif self.current_state == "ADMIN":
            print("_____________________\nADMIN MENU\n_____________________\n"
                  "0. Exit\n"
                  "1. About\n"
                  "2. Change admin's password\n"
                  "3. Output all users\n"
                  "4. Add new user\n"
                  "5. Block user\n"
                  "6. Enable/disable password constraint to user")
            chose = input()
            self.user_menu(chose)
        else:  # User mode
            print("_____________________\nUSER MENU\n_____________________\n"
                  "0. Exit\n"
                  "1. About\n"
                  "2. Change user's password")
            chose = input()
            self.user_menu(chose)

    def main_menu(self, chose):
        if chose == "0":
            print(Fore.BLUE, "Goodbye!")
            print(Style.RESET_ALL)
            self.exit_menu = True
        elif chose == "1":
            self.about()
        elif chose == "2":
            self.authorization()

        else:
            print(Fore.RED, "Incorrect input")
            print(Style.RESET_ALL)

    def about(self):
        print(Fore.GREEN, "Lab №1 made by Shcherbakova Yuliia IS-71\n"
                          "Task for password constraints: \n"
                          "Var22. Наявність латинських букв,"
                          " символів кирилиці, цифр і розділових знаків.")
        print(Style.RESET_ALL)

    def authorization(self):
        print("Input login: ")
        login = input()
        user_row = self.users.get_user_row(login)
        if user_row is None:
            print(Fore.RED, "Incorrect login. Try again")
            print(Style.RESET_ALL)
            self.main_menu("2")
        else:
            incorrect_password_count = 0
            while incorrect_password_count != 3:
                print("Input password: ")
                password = input()
                correct_password = check_password(user_row, password)
                if not correct_password:
                    if correct_password is None:
                        print(Fore.RED, "You are blocked!")
                        print(Style.RESET_ALL)
                        break
                    else:
                        print(Fore.LIGHTRED_EX, "Incorrect password")
                        print(Style.RESET_ALL)
                        incorrect_password_count += 1
                else:
                    self.current_state = login
                    break
            if incorrect_password_count == 3:
                print(Fore.RED, "Too many incorrect tries. Exiting...")
                print(Style.RESET_ALL)
                self.exit_menu = True

    def user_menu(self, chose):
        if chose == "0":
            print(Fore.BLUE, "Goodbye!")
            print(Style.RESET_ALL)
            self.exit_menu = True
        elif chose == "1":
            self.about()
        elif chose == "2":
            self.change_password_menu()
        elif self.current_state == "ADMIN":
            if chose == "3":
                print(Fore.GREEN, self.users.get_all_users())
                print(Style.RESET_ALL)
            elif chose == "4":
                print("Enter new user login:")
                login = input()
                if self.users.get_user_row(login) is not None:
                    print(Fore.YELLOW, "User already exists")
                    print(Style.RESET_ALL)
                    self.user_menu(chose)
                else:
                    self.users.add_user(login)
                    print(Fore.GREEN, "User ", login, " added successfully")
                    print(Style.RESET_ALL)
            elif chose == "5":
                print("Enter login of user you want to block:")
                login = input()
                if self.users.get_user_row(login) is None:
                    print(Fore.RED, "User doesn't exists")
                    print(Style.RESET_ALL)
                    self.user_menu(chose)
                else:
                    self.users.block_user(login)
                    print(Fore.GREEN, "User ", login, " is blocked")
                    print(Style.RESET_ALL)
            elif chose == "6":
                print("Enter login of user you want to enable/disable password constraint:")
                login = input()
                if self.users.get_user_row(login) is None:
                    print(Fore.RED, "User doesn't exists")
                    print(Style.RESET_ALL)
                    self.user_menu(chose)
                else:
                    self.users.change_constraint_to_user(login)
                    print(Fore.GREEN, "You have changed constraint parameters for user ", login)
                    print(Style.RESET_ALL)
        else:
            print(Fore.RED, "Incorrect input")
            print(Style.RESET_ALL)

    def change_password_menu(self):
        user_row = self.users.get_user_row(self.current_state)
        incorrect_password_count = 0
        old_password = ""
        while incorrect_password_count != 3:
            print("Input old password: ")
            old_password = input()
            correct_password = check_password(user_row, old_password)
            if not correct_password:
                print(Fore.LIGHTRED_EX, "Incorrect password")
                print(Style.RESET_ALL)
                incorrect_password_count += 1
            else:
                break
        if incorrect_password_count == 3:
            print(Fore.RED, "Too many incorrect tries. Exiting...")
            print(Style.RESET_ALL)
            self.exit_menu = True
            return
        new_password = self.get_new_password()
        if new_password is None:
            return

        confirm_password = None
        while confirm_password != new_password:
            if confirm_password is not None:
                print(Fore.RED, "New password and its confirmation should be equal")
                print(Style.RESET_ALL)
            print("Confirm new password: ")
            confirm_password = input()
        self.users.change_password(self.current_state, new_password)
        print(Fore.GREEN, "Password was changed successfully")
        print(Style.RESET_ALL)

    def new_password_menu(self):
        print("0. Exit\n"
              "1. Enter another password\n"
              "2. Don't change my password")
        chose = input()
        if chose == "0":
            self.exit_menu = True
        elif chose == "1":
            return self.get_new_password()
        elif chose == "2":
            return None
        else:
            print(Fore.RED, "Incorrect input")
            print(Style.RESET_ALL)
        return None

    def get_new_password(self):
        print("Input new password: ")
        new_password = input()
        if self.users.constraints_exist(self.current_state):
            if not Program_menu.password_is_valid(new_password):
                print(Fore.RED, "Password should consist of latin, "
                                "cyrillic, punctuation symbols and numbers")
                print(Style.RESET_ALL)
                return self.new_password_menu()
        return new_password

    def encrypt_and_save_changed_data(self):
        self.users.save()


    @staticmethod
    def password_is_valid(password):
        latin_symbols = re.search("[A-Za-z]", password)
        cyrillic_symbols = re.search("[А-Яа-я]", password)
        numbers = re.search("[0-9]", password)
        punctuation = re.search("[.,!?;:]", password)
        return latin_symbols and cyrillic_symbols and numbers and punctuation


def key_is_right():
    key = get_hashed_key()
    return compare_keys(key)


if __name__ == '__main__':
    colorama.init()
    if key_is_right():
        menu = Program_menu()
        while not menu.exit_menu:
            menu.show_menu()
        menu.encrypt_and_save_changed_data()
    else:
        print(Fore.RED, "You don't have rights to run this program")


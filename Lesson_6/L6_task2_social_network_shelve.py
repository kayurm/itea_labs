"""
Kateryna Yurmanovych
     lesson 6
     Task 2
REMAKE of the Social Network lab using Shelve as a DB.

Recap:
Existent(hardcoded) users and posts:
admin (pass: 1111----)
testuser (pass: 2222----)
testpost under testuser
"""

import re
import datetime
import yaml
import shelve
import uuid


class Base:

    def __init__(self):
        self._exit = False
        self._standard_user_logged_in = False
        self._admin_logged_in = False
        self._login = None

    def run(self):
        while not self._exit:
            Menu.show_main_menu(self)
            try:
                menu_option = int(input("\tEnter menu option (1-3):\n"))
            except ValueError or TypeError:
                print("Incorrect input. Please input exact 1,2 or 3 menu option.\n")
                continue

            # 1. AUTHORIZATION MODULE
            if menu_option == 1:
                auth = Authorization()
                authorized = auth.try_login()
                role = auth.get_user_role()
                if authorized and role == "standard":
                    self._standard_user_logged_in = True
                    self._login = auth.get_login()
                elif authorized and role == "admin":
                    self._admin_logged_in = True
                    self._login = auth.get_login()
                else:
                    self._standard_user_logged_in = False
                    self._admin_logged_in = False
                    self._login = None
                    print("Not authorized. You'll be redirected to the main menu.")
                    # return to the main menu
                    continue

            # 2. REGISTRATION MODULE
            if menu_option == 2:
                reg = Registration()
                try:
                    registered = reg.register()
                except Exception:
                    print("Something went wrong... You're being redirected to the main menu")
                    continue
                else:
                    if registered:
                        self._standard_user_logged_in = True
                        self._login = reg.get_login()
                    else:
                        self._standard_user_logged_in = False
                        self._login = None
                        # return to the main menu
                        continue

            # LOGGED IN -> STANDARD USER'S MENU MODULE
            if self._standard_user_logged_in:

                while True:
                    Menu.show_user_menu(self)
                    try:
                        user_menu_option = int(input("\tEnter menu option (1-3):\n"))
                    except ValueError or TypeError:
                        print("Incorrect input. Please input exact 1,2 or 3 menu option.\n")
                        continue

                    # to add a post
                    if user_menu_option == 1:
                        post = input("Enter your post: ")
                        DatabaseSingleton().add_post(self._login, post)

                    # to see the user's posts
                    elif user_menu_option == 2:
                        print("**** Your posts: ****")
                        for index, post in enumerate(DatabaseSingleton().get_posts_by_user(self._login)):
                            print(f"{index + 1}. ", post)

                    elif user_menu_option == 3:
                        self._standard_user_logged_in = False
                        break
                    else:
                        print("Incorrect user's menu choice.\n")
                        continue

            # ADMIN LOGGED IN -> ADMIN MENU MODULE
            if self._admin_logged_in:
                while True:
                    Menu.show_admin_menu(self)
                    try:
                        admin_menu_option = int(input("\tEnter menu option (1-3):\n"))
                    except ValueError or TypeError:
                        print("Incorrect input. Please input exact 1,2 or 3 menu option.\n")
                        continue

                    # to show all users
                    if admin_menu_option == 1:
                        print("\n**** All users: ****")
                        # using yaml (via PyYaml) for the pretty print
                        print(yaml.dump(DatabaseSingleton().get_users(), allow_unicode=True, default_flow_style=False))

                    # show all posts
                    elif admin_menu_option == 2:
                        print("\n**** All posts: ****")
                        print(yaml.dump(DatabaseSingleton().get_posts(), allow_unicode=True, default_flow_style=False))

                    elif admin_menu_option == 3:
                        self._admin_logged_in = False
                        break
                    else:
                        print("Incorrect user's menu choice.\n")
                        continue

            # 3. MAIN MENU EXIT
            if menu_option == 3:
                print("See you!")
                self._exit = True

            if menu_option not in (1, 2, 3):
                print("Incorrect menu choice.\n")
                continue


class Menu:

    @staticmethod
    def show_main_menu(self):
        print("\n*** Main Menu *********")
        print("*** 1) Login      *****")
        print("*** 2) Register   *****")
        print("*** 3) Exit       *****")
        print("***********************")

    @staticmethod
    def show_user_menu(self):
        print("\n*** User Menu *********")
        print("*** 1) Enter post    **")
        print("*** 2) See your posts *")
        print("*** 3) Log out       **")
        print("***********************")

    @staticmethod
    def show_admin_menu(self):
        print("\n*** Admin Menu ********")
        print("*** 1) Show users   ***")
        print("*** 2) Show posts   ***")
        print("*** 3) Log out      ***")
        print("***********************")


class Registration:

    def __init__(self):
        self._reg_login = None
        self.role = "standard"

    def register(self):
        while True:
            self._reg_login = input("Enter login: ")
            if len(self._reg_login) < 1:
                print("You didn't enter your login name. Try again.")
                continue
            if self._reg_login in DatabaseSingleton.get_users(DatabaseSingleton()):
                print("Login already exists, please enter another one: ")
                continue
            while True:
                reg_password = input("Enter password (should be min 8 chars long and contain digits,symbols): ")
                numbers_fault = re.search(r"\d", reg_password) is None
                symbols_fault = re.search(r"[!#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', reg_password) is None
                length_fault = len(reg_password) < 8
                if numbers_fault or symbols_fault or length_fault:
                    print("Password doesn't satisfy the strength criteria. It should be min 8 chars long and contain "
                          "digits,symbols. Try again. ")
                    continue
                else:
                    repeat_password = input("Enter password again: ")
                    if repeat_password != reg_password:
                        print("Passwords don't match. Try again.")
                        continue
                    else:
                        print("You've been successfully registered.")
                        DatabaseSingleton().add_user(self._reg_login, reg_password, self.role)
                        return True

    def get_login(self):
        return self._reg_login


class Authorization:
    _login = None

    @classmethod
    def try_login(cls):
        users_dict = DatabaseSingleton().get_users()
        while True:
            login_in = input("Enter login: ")
            password_in = input("Enter password: ")

            # authorized scenario:
            if login_in in users_dict.keys():
                user_record = users_dict.get(login_in)
                if user_record["password"] == password_in:
                    cls._login = login_in
                    print("Logged in successfully.")
                    return True

            # (else) not authorized scenario:
            print("Login/password incorrect.")
            again = input("Want to try again? Y/N")
            if again == "y" or again == "Y":
                continue
            else:
                return False

    @classmethod
    def get_login(cls):
        return cls._login

    @classmethod
    def get_user_role(cls):
        return "admin" if cls._login == "admin" else "standard"


# Class - Database containing users and posts and their getters/setters
class DatabaseSingleton:
    instance = None
    _users_dict = dict()
    _admin = {"password": "1111----", "role": "admin"}
    _test_user = {"password": "2222----", "role": "standard"}
    _posts_dict = dict()
    _post_id = str(uuid.uuid4())
    _testpost = {"login": "testuser", "post": "this is a test post"}

    def __new__(cls):
        if cls.instance:
            return cls.instance
        cls.instance = super().__new__(cls)
        cls.instance._users_dict["admin"] = cls._admin
        cls.instance._users_dict["testuser"] = cls._test_user
        cls.instance._posts_dict[cls._post_id] = cls._testpost
        with shelve.open("shelf_users", writeback=True) as sh:
            if len(sh) == 0:
                sh.update(cls.instance._users_dict)
        with shelve.open("shelf_posts", writeback=True) as sh:
            if len(sh) == 0:
                sh.update(cls.instance._posts_dict)

        return cls.instance

    def get_users(self):
        with shelve.open("shelf_users", writeback=True) as sh:
            self._users_dict = dict(sh)
        return self._users_dict

    def add_user(self, login, password, role):
        record = {
            "password": password,
            "role": role,
            "reg_date": datetime.datetime.now()
        }
        with shelve.open("shelf_users", writeback=True) as sh:
            sh[login] = record

    def add_post(self, login, post_body):
        self._post_id = str(uuid.uuid4())
        post = {
            "login": login,
            "post": post_body,
            "post_date": datetime.datetime.now()
        }
        with shelve.open("shelf_posts", writeback=True) as sh:
            sh[self._post_id] = post
        print("Your post was added.")

    def get_posts(self):
        with shelve.open("shelf_posts", writeback=True) as sh:
            self._posts_dict = dict(sh)
        return self._posts_dict

    def get_posts_by_user(self, login):
        users_posts = []
        with shelve.open("shelf_posts", writeback=True) as sh:
            self._posts_dict = dict(sh)
        for record in self._posts_dict.values():
            if record["login"] == login:
                users_posts.append(record["post"])
        return users_posts


if __name__ == "__main__":
    Base().run()

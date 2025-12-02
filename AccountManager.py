import re
import os
import shutil
import platform
import ctypes
from argon2 import PasswordHasher, exceptions


def has_special_char(text):
    # check for characters that are not alphabetical, numerical, or an underscore
    pattern = r'[^a-zA-Z0-9_]'
    return bool(re.search(pattern, text))


def is_valid_password(password):
    # password is at least 8 chars
    if len(password) < 8:
        return "short_password"
    # password must have a special char
    if not has_special_char(password):
        return "no_special_char"
    return "valid"


def get_hash(username):
    # retrieve hashed password
    try:
        with open(f"users/{username}/pass.bin", "r") as file:
            return file.readline()
    except FileNotFoundError:
        return None


def check_password(ph, hashed, password):
    # verify password is correct
    try:
        ph.verify(hashed, password)
        return True
    except exceptions.VerifyMismatchError:
        return False


class AccountManager:
    def __init__(self, username=None):
        self.__username = username

    # returns True if success, False if fail
    def add_account(self, username, password):
        # username is at least 4 chars
        if len(username) < 4:
            return "short_username"

        # username must not have special char
        if has_special_char(username):
            return "user_has_special_char"

        valid = is_valid_password(password)
        if valid != "valid":
            return valid

        # check if username already exists
        try:
            os.mkdir(f"users/{username}")
            os.mkdir(f"users/{username}/data")
            os.mkdir(f"users/{username}/data/code")
            os.mkdir(f"users/{username}/data/graphs")
            with open(f"users/{username}/data/history_log.txt", "w") as file:
                pass

        except FileExistsError:
            return "user_alr_exists"

        # store password as a hash
        with open(f"users/{username}/pass.bin", "wb") as file:
            ph = PasswordHasher()
            hashed = ph.hash(password)
            file.write(hashed.encode("utf-8"))

        # hide file
        if platform.system() == "Windows":
            ctypes.windll.kernel32.SetFileAttributesW(f"users/{username}/pass.bin", 2)

        self.__username = username
        return "success"

    def delete_account(self, username, password):
        # verify username
        hashed = get_hash(username)
        if hashed is None:
            return "user_does_not_exist"

        # verify password
        ph = PasswordHasher()
        if check_password(ph, hashed, password):
            # delete user files
            shutil.rmtree(f"users/{username}")
            self.__username = None
            return "success"
        else:
            return "incorrect_password"

    def login(self, username, password):
        # verify username
        hashed = get_hash(username)
        if hashed is None:
            return False

        # verify password
        ph = PasswordHasher()
        if check_password(ph, hashed, password):
            # login
            self.__username = username
            return True
        else:
            return False

    def change_password(self, username, old_password, new_password):
        if not self.login(username, old_password):
            return "invalid_info"

        if old_password == new_password:
            return "new_equals_old"

        valid = is_valid_password(new_password)
        if valid != "valid":
            return valid

        # reveal file
        if platform.system() == "Windows":
            ctypes.windll.kernel32.SetFileAttributesW(f"users/{username}/pass.bin", 0)
        with open(f"users/{username}/pass.bin", "wb") as file:
            file.truncate()
            ph = PasswordHasher()
            hashed = ph.hash(new_password)
            file.write(hashed.encode("utf-8"))
        # hide file
        if platform.system() == "Windows":
            ctypes.windll.kernel32.SetFileAttributesW(f"users/{username}/pass.bin", 2)

        return "success"

    def get_history_log(self):
        """Reads history log into a list
        :return: a list of strings representing history items from oldest to most recent
        """
        history = []
        with open(f"users/{self.__username}/data/history_log.txt", "r") as log:
            item = log.readline()
            while item != "":
                history.append(item[:-1])
                item = log.readline()
        return history

    def get_code_file_path(self, item_name):
        """Returns file path for saved code"""
        return f"users/{self.__username}/data/code/{item_name}.py"

    def get_graph_file_path(self, item_name):
        """Returns file path for saved graph"""
        return f"users/{self.__username}/data/graphs/{item_name}.png"

    def add_history_item(self, item_name, graph_displayer):
        """Adds item to user history
        Call this function after time complexity analysis and graphing have finished
        :param item_name: string filename w/o extension (e.g. bubble_sort)
        :param graph_displayer: GraphDisplayer object
        """
        graph_displayer.save_graph(self.get_graph_file_path(item_name))  # save graph
        with open(f"users/{self.__username}/data/history_log.txt", "a") as log:  # write to log
            log.write(item_name + "\n")

    def delete_history_item(self, item_name):
        """Deletes item (including code and graph) from user history
        :param item_name: string filename w/o extension (e.g. bubble_sort)
        """
        os.remove(f"users/{self.__username}/data/code/{item_name}.py")  # delete code
        os.remove(f"users/{self.__username}/data/graphs/{item_name}.png")  # delete graph
        with open(f"users/{self.__username}/data/history_log.txt", "r") as log:  # delete from log
            log_data = log.read()
        with open(f"users/{self.__username}/data/history_log.txt", "w") as log:
            log.write(log_data.replace(f"{item_name}\n", ""))

    def clear_history(self):
        """Removes all history data"""
        shutil.rmtree(f"users/{self.__username}/data/code")  # delete all data
        shutil.rmtree(f"users/{self.__username}/data/graphs")
        with open(f"users/{self.__username}/data/history_log.txt", "w") as log:  # clear history log
            log.write("")
        os.mkdir(f"users/{self.__username}/data/code")  # create empty directories
        os.mkdir(f"users/{self.__username}/data/graphs")

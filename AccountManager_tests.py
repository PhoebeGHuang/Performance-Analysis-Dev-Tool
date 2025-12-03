from unittest import TestCase
from AccountManager import AccountManager
import os


class TestAccountManager(TestCase):
    def test_add_account(self):
        am = AccountManager()

        # add account
        val = am.add_account("New_User123", "password123!")
        self.assertTrue(val)

        # make sure directory exists
        val = os.path.isdir("users/New_User123")
        self.assertTrue(val)

        # delete account
        am.delete_account("New_User123", "password123!")

    def test_invalid_username(self):
        am = AccountManager()

        # test short username
        val = am.add_account("aaa", "password123!")
        self.assertEqual("short_username", val)

        # test username with special chars
        val = am.add_account("%User%", "password123!")
        self.assertEqual("user_has_special_char", val)

    def test_invalid_password(self):
        am = AccountManager()

        # test short password
        val = am.add_account("User123", "pass!")
        self.assertEqual("short_password", val)

        # test password with no special chars
        val = am.add_account("User123", "good_password")
        self.assertEqual("no_special_char", val)

    def test_delete_account(self):
        am = AccountManager()

        # test nonexistent user
        val = am.delete_account("I_do_not_exist", "password123!")
        self.assertFalse(val)

        # test invalid password
        am.add_account("New_User123", "password123!")
        val = am.delete_account("New_User123", "wrong_password!")
        self.assertFalse(val)

        # test valid password
        val = am.delete_account("New_User123", "password123!")
        self.assertTrue(val)

    def test_login(self):
        am = AccountManager()
        am.add_account("New_User123", "password123!")

        # test invalid user
        val = am.login("New_User321", "password123!")
        self.assertFalse(val)

        # test invalid password
        val = am.login("New_User321", "wrong_password!")
        self.assertFalse(val)

        # test correct info
        val = am.login("New_User123", "password123!")
        self.assertTrue(val)

        am.delete_account("New_User123", "password123!")

    def test_change_password(self):
        am = AccountManager()
        am.add_account("New_User123", "password123!")

        # test invalid old password
        val = am.change_password("New_User123", "old_password!", "new_password!")
        self.assertEqual("invalid_info", val)

        # test same old/new password
        val = am.change_password("New_User123", "password123!", "password123!")
        self.assertEqual("new_equals_old", val)

        # test invalid new password
        val = am.change_password("New_User123", "password123!", "pass!")
        self.assertEqual("short_password", val)
        val = am.change_password("New_User123", "password123!", "new_password")
        self.assertEqual("no_special_char", val)

        # test successful
        val = am.change_password("New_User123", "password123!", "new_password123!")
        self.assertEqual("success", val)

        am.delete_account("New_User123", "new_password123!")

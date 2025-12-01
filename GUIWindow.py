import tkinter as tk
from LoginScreen import LoginScreen
from CodeDisplayer import CodeDisplayer
from AccountManager import AccountManager


class GUIWindow:
    def __init__(self):
        # main Tk window
        self.root = tk.Tk()
        self.root.title("Optimizer Dev Tool")
        self.root.geometry("1280x720")

        # one shared AccountManager
        self.account_manager = AccountManager()

        self.current_screen = None
        self.username = None

        # start on login screen
        self.show_login_screen()

        # start event loop
        self.root.mainloop()

    # screen switching helpers
    def clear_screen(self):
        if self.current_screen is not None:
            self.current_screen.destroy()
            self.current_screen = None

    def show_login_screen(self):
        self.clear_screen()
        self.current_screen = LoginScreen(
            master=self.root,
            gui_window=self,
            account_manager=self.account_manager
        )
        self.current_screen.pack(fill="both", expand=True)

    def show_main_tool(self, username):

        self.username = username
        self.clear_screen()

        # main performance analysis GUI
        self.current_screen = CodeDisplayer(
            username=self.username,
            master=self.root,
            account_manager=self.account_manager,
            gui_window=self,
        )
        self.current_screen.pack(fill="both", expand=True)

        self.root.title(f"Optimizer Dev Tool — {self.username}")



import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class LoginScreen(ttk.Frame):
    def __init__(self, master, gui_window, account_manager):
        super().__init__(master)
        self.master = master
        self.gui_window = gui_window
        self.account_manager = account_manager

        self.build_ui()

    def build_ui(self):
        self.master.title("Optimizer Dev Tool: Login")
        self.master.geometry("1200x700")
        self.master.configure(bg="#f5f5f5")

        # main container
        main = tk.Frame(self, bg="#f5f5f5")
        main.pack(fill="both", expand=True)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # left panel
        left_panel = tk.Frame(main, bg="black")
        left_panel.grid(row=0, column=0, sticky="nsew")

        img = Image.open("leftpanel.png")
        img = img.resize((600, 700))  # adjust to fit
        self.bg_image = ImageTk.PhotoImage(img)

        bg_label = tk.Label(left_panel, image=self.bg_image, bg="black")
        bg_label.place(relwidth=1, relheight=1)

        # right login panel
        right_panel = tk.Frame(main, bg="#f5f5f5")
        right_panel.grid(row=0, column=1, sticky="nsew")

        form = tk.Frame(right_panel, bg="#f5f5f5")
        form.place(relx=0.5, rely=0.5, anchor="center")

        # title
        tk.Label(
            form,
            text="Log in",
            font=("Segoe UI", 22, "bold"),
            bg="#f5f5f5"
        ).pack(pady=(0, 25))

        # username
        tk.Label(form, text="Username", font=("Segoe UI", 11), bg="#f5f5f5").pack(anchor="w")
        self.username_entry = ttk.Entry(form, width=30)
        self.username_entry.pack(pady=(0, 15))

        # password
        tk.Label(form, text="Password", font=("Segoe UI", 11), bg="#f5f5f5").pack(anchor="w")
        self.password_entry = ttk.Entry(form, width=30, show="•")
        self.password_entry.pack(pady=(0, 20))

        ttk.Button(
            form,
            text="Log In",
            command=self.attempt_login,
            width=20
        ).pack(pady=(0, 8))

        ttk.Button(
            form,
            text="Create Account",
            command=self.create_account,
            width=20
        ).pack()

        self.pack(fill="both", expand=True)

    # login logic
    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return

        success = self.account_manager.login(username, password)

        if success:
            # switch to main tool screen
            self.gui_window.show_main_tool(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


    # create account logic
    def create_account(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Create Account Error", "Enter a username and password first.")
            return

        created = self.account_manager.add_account(username, password)

        if created:
            messagebox.showinfo(
                "Account Created",
                "Account created successfully. You may now log in."
            )
        else:
            messagebox.showerror(
                "Create Account Failed",
                "Username already exists or does not meet the required format.\nPlease check the guidelines."
            )

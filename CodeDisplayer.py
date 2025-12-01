import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
from tkinter import filedialog, ttk, messagebox, simpledialog
import os
from CodeHighlighter import CodeHighlighter
from AlgorithmDescriber import AlgorithmDescriber
from HistoryViewer import HistoryViewer
from HelpMenu import HelpMenu


class CodeDisplayer(tk.Frame):
    def __init__(self, username, master=None, account_manager=None, gui_window=None):
        super().__init__(master)
        self.username = username
        self.master = master
        self.master.title("Optimizer Dev Tool")
        self.master.geometry("1280x720")
        self.account_manager = account_manager
        self.gui_window = gui_window
        self.history_viewer = HistoryViewer(self.master, self.account_manager, self)
        self.algorithm_describer = AlgorithmDescriber()
        self.help_menu = HelpMenu(self.master)

        # frame for text area and scrollbars
        text_frame = ttk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # vertical scrollbar
        y_scroll = ttk.Scrollbar(text_frame, orient="vertical")
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # horizontal scrollbar
        x_scroll = ttk.Scrollbar(text_frame, orient="horizontal")
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # text area
        self.text_area = tk.Text(
            text_frame,
            wrap="none",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            font=("Consolas", 12),
            background="#1e1e1e",  # dark box
            foreground="#dcdcdc",  # light text
            insertbackground="white",  # white cursor
            relief="flat",
            borderwidth=0
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # links scrollbars
        y_scroll.config(command=self.text_area.yview)
        x_scroll.config(command=self.text_area.xview)

        # file tracking
        self.file_path = None

        # right side buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.Y, side=tk.RIGHT, padx=10, pady=10)

        # function buttons
        ttk.Button(button_frame, text="Open File", command=self.get_code).pack(pady=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_contents).pack(pady=5)
        ttk.Button(button_frame, text="Submit", command=self.submit_code).pack(pady=5)
        ttk.Button(button_frame, text="History",
                   command=lambda: self.history_viewer.show_history_popup()).pack(pady=5)

        # instructional section
        ttk.Separator(button_frame, orient="horizontal").pack(fill="x", pady=(25, 10))
        ttk.Label(button_frame, text="Student Guide", font=("Segoe UI", 10, "italic"), foreground="#666").pack(
            anchor="center", pady=(0, 5))

        # standard algorithms button
        ttk.Button(button_frame, text="Standard Algorithms",
                   command=lambda: self.algorithm_describer.show_popup(self.master), width=15).pack(pady=5)

        # standard algorithms graph button
        ttk.Button(button_frame, text="Complexities Graph",
                   command=self.show_complexity_graph, width=15).pack(pady=5)

        # help menu
        ttk.Button(button_frame, text="User Guide",
                   command=lambda: self.help_menu.show_help_popup(), width=15).pack(pady=5)

        # account management section
        ttk.Separator(button_frame, orient="horizontal").pack(fill="x", pady=(25, 10))
        ttk.Label(button_frame, text="Account Settings",
                  font=("Segoe UI", 10, "italic"), foreground="#666").pack(anchor="center", pady=(0, 5))

        ttk.Button(button_frame, text="Change Password",
                   command=self.change_password).pack(pady=5)

        ttk.Button(button_frame, text="Delete Account",
                   command=self.delete_account).pack(pady=5)


        # instructional note about upload or typing
        usage_note = ttk.Label(
            button_frame,
            text="You can upload a code file or paste code directly.",
            foreground="#555",
            font=("Segoe UI", 10, "italic"),
            justify="left",
            wraplength=200
        )
        usage_note.pack(pady=(15, 0), anchor="w")

        # instructional note about main files
        note_label = ttk.Label(
            button_frame,
            text="Note: Only upload files containing a main() function.\n\n"
                 "The analyzer measures performance on the main execution block.",
            foreground="#555",
            font=("Segoe UI", 10, "italic"),
            justify="left",
            wraplength=200
        )
        note_label.pack(pady=(10, 0), anchor="w")

    # file operations
    def get_code(self):
        # open file explorer to select code file
        file_path = filedialog.askopenfilename(
            title="Select a Python file",
            filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            self.file_path = file_path
            self.display_contents()  # auto display file content
            filename = os.path.basename(file_path)
            self.master.title(f"Optimizer Dev Tool: {filename}")  # update title

    def display_contents(self):
        # displays selected file contents in text area
        if not self.file_path:
            self.text_area.insert(tk.END, "No file selected.\n")
            return
        try:
            with open(self.file_path, "r") as file:
                code = file.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, code)
        except Exception as e:
            self.text_area.insert(tk.END, f"Error loading file: {e}\n")

    def clear_contents(self):
        # clears text area
        self.text_area.delete("1.0", tk.END)

    def submit_code(self):
        # make sure text area isn't empty
        content = self.text_area.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showinfo("Could not submit", "Text entry field is empty!")
            return

        else:
            # ask user to name program
            program_name = simpledialog.askstring(
                title="Program name",
                prompt="Enter a name for your program (name will be stored in history):",
                parent=self.master
            )

            # check if code needs input
            inputs = []
            while True:
                num_inputs = simpledialog.askstring(
                    title="Number of inputs",
                    prompt="How many inputs does your program need? (Type a positive integer, or 0)",
                    parent=self.master
                )
                # exits if user clicks cancel
                if num_inputs is None:
                    return
                # make sure input is valid
                try:
                    num_inputs = int(num_inputs)
                    if num_inputs < 0:
                        continue
                    break
                except ValueError:
                    continue

            # prompt user for required inputs to run program
            needs_input = num_inputs > 0
            if needs_input:
                suffixes = {1: "st", 2: "nd", 3: "rd"}
                for i in range(num_inputs):
                    if 10 <= (i + 1) % 100 <= 20:
                        suffix = "th"
                    else:
                        suffix = suffixes.get((i + 1) % 10, "th")

                    user_input = simpledialog.askstring(
                        title=f"Input #{i + 1}",
                        prompt=f"What is the {i + 1}{suffix} input in your program?",
                        parent=self.master
                    )

                    if user_input is None:
                        return
                    inputs.append(user_input)

            selection = CodeHighlighter(self.text_area, program_name, needs_input, inputs, self.account_manager)
            selection.submit_selection()

    # complexities graph
    def show_complexity_graph(self):
        graph_path = "graph_common_time_complexities.png"

        window = Toplevel(self.master)
        window.title("Common Time Complexities Graph")

        try:
            img = Image.open(graph_path)
            tk_img = ImageTk.PhotoImage(img)

            label = tk.Label(window, image=tk_img)
            label.image = tk_img
            label.pack()

        except Exception as e:
            tk.Label(window, text=f"Error loading graph: {e}").pack()


    def change_password(self):
        if not self.username:
            messagebox.showerror("Error", "No user is currently logged in.")
            return

        username = self.username

        old_pw = simpledialog.askstring(
            "Change Password",
            "Enter your current password:",
            show="•",
            parent=self.master
        )
        if old_pw is None:
            return

        new_pw = simpledialog.askstring(
            "Change Password",
            "Enter your new password:",
            show="•",
            parent=self.master
        )
        if new_pw is None:
            return

        confirm_pw = simpledialog.askstring(
            "Change Password",
            "Re-enter your new password:",
            show="•",
            parent=self.master
        )
        if confirm_pw is None:
            return

        if new_pw != confirm_pw:
            messagebox.showerror("Change Password Failed", "New passwords do not match.")
            return

        success = self.account_manager.change_password(username, old_pw, new_pw)

        if success:
            messagebox.showinfo("Password Changed", "Your password has been successfully updated.")
        else:
            messagebox.showerror(
                "Change Password Failed",
                "Password could not be changed.\n"
                "Check your current password and make sure the new one meets the requirements."
            )


    def delete_account(self):
        if not self.username:
            messagebox.showerror("Error", "No user is currently logged in.")
            return

        username = self.username

        confirm = messagebox.askyesno(
            "Delete Account",
            f"Are you sure you want to permanently delete the account '{username}'?\n"
            "This action cannot be undone."
        )
        if not confirm:
            return

        pw = simpledialog.askstring(
            "Confirm Password",
            "Enter your password to confirm account deletion:",
            show="•",
            parent=self.master
        )
        if pw is None:
            return

        success = self.account_manager.delete_account(username, pw)

        if success:
            messagebox.showinfo(
                "Account Deleted",
                "Your account has been deleted."
            )
            if self.gui_window is not None:
                # reset GUIWindow state & go back to log in
                self.gui_window.username = None
                self.gui_window.show_login_screen()
        else:
            messagebox.showerror(
                "Delete Account Failed",
                "Account could not be deleted.\nYour password may be incorrect."
            )





# test
# if __name__ == "__main__":
    # root = tk.Tk()
    # am = AccountManager()
    # gd = GraphDisplayer()
    # app = CodeDisplayer(master=root, account_manager=am, graph_displayer=gd)
    # app.pack(fill=tk.BOTH, expand=True)
    # root.mainloop()

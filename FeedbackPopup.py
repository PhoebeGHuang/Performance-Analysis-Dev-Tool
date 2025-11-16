import tkinter as tk
from tkinter import ttk

class FeedbackPopup:
    """
        displays feedback messages or analysis results in a popup window
        can be used to show errors, warnings, or success notifications
        after Analyzer or BigOCalculator execution
        """


    @staticmethod
    def show_message(message, title="Info"):
        popup = tk.Toplevel()
        popup.title("Optimizer Dev Tool - Feedback")
        popup.geometry("380x220")
        popup.configure(bg="#1e1e1e")
        popup.resizable(False, False)

        # outer frame
        frame = tk.Frame(popup, bg="#2a2a2a", bd=2, relief="flat")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=160)

        # title
        title_label = tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 13, "bold"),
            fg="#4da6ff",
            bg="#2a2a2a"
        )
        title_label.pack(pady=(15, 5))

        # message text
        msg_label = tk.Label(
            frame,
            text=message,
            font=("Segoe UI", 11),
            fg="#e6e6e6",
            bg="#2a2a2a",
            wraplength=260,
            justify="center"
        )
        msg_label.pack(pady=(0, 15))

        # close button
        close_btn = tk.Button(
            frame,
            text="Close",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#000000",
            activebackground="#dcdcdc",
            activeforeground="#000000",
            relief="flat",
            width=12,
            command=popup.destroy
        )
        close_btn.pack()

        popup.grab_set()


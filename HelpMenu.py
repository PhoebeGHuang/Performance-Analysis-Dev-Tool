import tkinter as tk
from tkinter import ttk


class HelpMenu:
    def __init__(self, master):
        self.master = master

    def show_help_popup(self):
        win = tk.Toplevel(self.master)
        win.title("Help & User Guide")
        win.geometry("700x600")

        container = ttk.Frame(win, padding=15)
        container.pack(fill="both", expand=True)

        title = ttk.Label(
            container,
            text="Optimizer Dev Tool: User Guide",
            font=("Segoe UI", 16, "bold")
        )
        title.pack(pady=(0, 10))

        text = tk.Text(
            container,
            wrap="word",
            font=("Segoe UI", 11),
            height=15
        )
        text.pack(fill="both", expand=True)

        help_content = """
Welcome to the Optimizer Dev Tool.

How to Use:
1. Upload a code file or paste in code containing a main() function.
2. Click 'Submit' to run performance analysis.
3. The system will:
   - Measure execution time
   - Calculate Big-O complexity
   - Display a runtime graph

Key Buttons:
• Open File – Load a Python file
• Submit – Evaluate runtime complexity
• Clear – Clears code
• Standard Algorithms – Shows time complexity references
• Complexities Graph – Shows common Big-O curves

Notes:
- Your code must include a main() function.
- Input prompts will appear if your program requires values.
- All runs are saved in your account history.

        """

        text.insert("1.0", help_content)
        text.config(state="disabled")


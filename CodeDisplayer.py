import tkinter as tk
from tkinter import filedialog, ttk
import os

class CodeDisplayer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Optimizer Dev Tool")
        self.master.geometry("900x600")

        # frame for text area and scrollbars
        text_frame = ttk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # vertical scrollbar
        y_scroll = ttk.Scrollbar(text_frame, orient="vertical")
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # horizontal scrollbar (now spans entire bottom)
        x_scroll = ttk.Scrollbar(self.master, orient="horizontal")
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # text area
        self.text_area = tk.Text(
            text_frame,
            wrap="none",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            font=("Consolas", 12),
            background="#1e1e1e",      # dark box
            foreground="#dcdcdc",      # light text
            insertbackground="white",  # white cursor
            relief="flat",
            borderwidth=0
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # link scrollbars
        y_scroll.config(command=self.text_area.yview)
        x_scroll.config(command=self.text_area.xview)

        # file tracking
        self.file_path = None

        # right side buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.Y, side=tk.RIGHT, padx=10, pady=10)

        ttk.Button(button_frame, text="Open File", command=self.get_code).pack(pady=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_contents).pack(pady=5)

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


# test
if __name__ == "__main__":
    root = tk.Tk()
    app = CodeDisplayer(master=root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
import os
import ErrorChecker


class CodeHighlighter:
    def __init__(self, text_area, needs_input, inputs):
        try:
            # get selected text if possible
            self.selected_text = text_area.get("sel.first", "sel.last")
        except tk.TclError:
            # select everything instead
            self.selected_text = text_area.get("1.0", "end-1c").strip()
        self.needs_input = needs_input
        self.inputs = inputs

    def submit_selection(self):
        # submits code to be analyzed
        try:
            with open("data/submission.py", "w+") as file:
                file.write(self.selected_text)
                # make sure file is written before program continues
                file.flush()
                os.fsync(file.fileno())

                # check for errors in user code
                ec = ErrorChecker.ErrorChecker("data/submission.py")
                if not ec.detect_syntax_errors():
                    runtime_result = ec.detect_infinite_loops(self.needs_input, self.inputs)
                    if not ec.err == "":
                        messagebox.showerror(runtime_result, f"Your program could not run properly:\n\n{ec.err}")
                else:
                    messagebox.showerror("Syntax error found in your program", ec.err)

        except Exception as e:
            messagebox.showerror(e, "Error submitting file")

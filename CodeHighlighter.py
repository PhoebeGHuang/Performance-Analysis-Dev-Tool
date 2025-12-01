import tkinter as tk
from tkinter import messagebox
import os
from Analyzer import Analyzer
from FeedbackPopup import FeedbackPopup
from GraphDisplayer import GraphDisplayer


class CodeHighlighter:
    def __init__(self, text_area, needs_input, inputs):
        try:
            # get selected text if possible
            self.selected_text = text_area.get("sel.first", "sel.last")
            if self.selected_text[:4] != "    ":
                self.selected_text = "    " + self.selected_text
            self.selected = True
        except tk.TclError:
            # select everything instead
            self.selected_text = text_area.get("1.0", "end-1c").strip()
            self.selected = False
        self.needs_input = needs_input
        self.inputs = inputs

    def submit_selection(self):
        # submits code to be analyzed
        try:
            with open("data/submission.py", "w+") as file:
                if self.selected:
                    file.write("n = 1\ndef main():\n")
                file.write(self.selected_text)
                if self.selected:
                    file.write("\nmain()")
                # make sure file is written before program continues
                file.flush()
                os.fsync(file.fileno())

                # create analyzer object
                an = Analyzer(program="data/submission.py",
                              n="n",
                              needs_input=self.needs_input,
                              inputs=self.inputs)

                # check for errors in user code
                ec = an.error_check
                if not ec.detect_syntax_errors():
                    runtime_result = ec.detect_infinite_loops()
                    if not ec.err == "":
                        messagebox.showerror(runtime_result, f"Your program could not run properly:\n\n{ec.err}")
                    else:
                        complexity = an.calc.calculate()
                        FeedbackPopup.show_message("The time complexity of the code is " + complexity)
                        gd = GraphDisplayer()
                        gd.create_graph(timing_data=an.calc.get_time_data(), complexity_label=complexity)
                else:
                    messagebox.showerror("Syntax error found in your program", ec.err)

        except Exception as e:
            messagebox.showerror("Error submitting file", e)

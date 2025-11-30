import tkinter as tk
from tkinter import ttk


class HistoryViewer:
    def __init__(self, master, account_manager, code_displayer, graph_displayer):
        self.master = master
        self.account_manager = account_manager
        self.code_displayer = code_displayer
        self.graph_displayer = graph_displayer

    def show_history_popup(self):
        """Displays user history and allows user to select an item"""
        # create window
        win = tk.Toplevel(self.master)
        win.title("History")
        win.geometry("200x200")

        # create frame inside window
        frame = ttk.Frame(win, padding=(3, 3, 3, 3))
        frame.grid(column=0, row=0, columnspan=2, rowspan=2)

        # create list view of user history
        history = self.account_manager.get_history_log()
        history.reverse()  # reverse history so that newest shows first
        historyvar = tk.StringVar(value=history)
        lb = tk.Listbox(frame, listvariable=historyvar, height=8)
        lb.grid(column=0, row=0, columnspan=2)

        # create view button
        view_btn = ttk.Button(frame, text="View", default="active",
                              command=lambda: self.display_item(lb, history))
        win.bind("<Return>", lambda f: view_btn.invoke())
        view_btn.grid(column=0, row=1)

        # create delete button
        delete_btn = ttk.Button(frame, text="Delete",
                                command=lambda: self.delete_item(lb, history))
        delete_btn.grid(column=1, row=1)

    def display_item(self, listbox, history):
        if len(listbox.curselection()) == 1:
            item = history[int(listbox.curselection()[0])]
            self.code_displayer.file_path = self.account_manager.get_code_file_path(item)
            self.code_displayer.display_contents()
            graph = self.account_manager.get_graph_file_path(item)
            self.graph_displayer.load_graph(graph)
        else:
            return

    def delete_item(self, listbox, history):
        if len(listbox.curselection()) == 1:
            item = history[int(listbox.curselection()[0])]
            self.account_manager.delete_history_item(item)
        else:
            return

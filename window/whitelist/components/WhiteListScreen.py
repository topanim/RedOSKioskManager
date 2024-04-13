import tkinter as tk
from json import loads, dumps
from tkinter import ttk

from window.whitelist.components.WhiteListTable import WhiteListTable


class WhiteListScreen(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.domain_var = tk.StringVar()
        self.table = WhiteListTable(self)
        self.domains = []

    def save_domains(self):
        # TODO: replace .. to window/whitelist
        with open('../config/whitelist.json', 'w', encoding='utf-8') as f:
            f.write(dumps(self.table.get_domains(), ensure_ascii=False))

    @staticmethod
    def get_saved():
        with open('../config/whitelist.json', 'r', encoding='utf-8') as f:
            try:
                domains = [str(obj) for obj in loads(f.read())]
            except:
                domains = []

        return domains

    def load_domains(self):
        domains = self.get_saved()

        self.clear_domains()
        for domain in domains:
            self.table.add_item(domain)

    def clear_domains(self):
        self.table.delete_all_items()

    def confirm(self, event=None):
        self.table.add_item(self.domain_var.get())
        self.domain_var.set('')

    def init(self):
        self.pack()

        self.table.init()
        self.load_domains()

        input_row = tk.Frame()
        input_row.pack()

        domain_entry = ttk.Entry(input_row, style="TEntry", textvariable=self.domain_var)
        domain_entry.bind("<Return>", self.confirm)
        domain_entry.pack(side=tk.LEFT, padx=8)

        write_entry = ttk.Button(input_row, text=">", command=self.confirm)
        write_entry.pack(side=tk.LEFT)

        save = ttk.Button(self, text="save", command=self.save_domains)
        save.pack()


# root = tk.Tk()
# WhiteListScreen(root).init()
# root.mainloop()

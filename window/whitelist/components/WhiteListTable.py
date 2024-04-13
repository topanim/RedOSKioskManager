from tkinter import ttk
import tkinter as tk

from utils.is_not_empty import is_not_empty


class WhiteListTable(ttk.Treeview):
    def __init__(self, master=None):
        super().__init__(
            master,
            columns=('domain',),
            show='headings'
        )
        self.heading('domain', text='Domain')
        self.domains = set()

    def get_domains(self):
        return list(self.domains)

    def item_select(self, _):
        for i in self.selection():
            pass

    def delete_all_items(self):
        for row_id in self.get_children():
            self.delete_item(row_id)

    def delete_item(self, _id):
        domain = self.item(_id)['values'][0]
        self.domains.remove(domain)
        self.delete(_id)

    def delete_selected_items(self, _):
        print('delete')
        for selection in self.selection():
            self.delete_item(selection)

    def add_item(self, domain: str):
        if domain not in self.domains and is_not_empty(domain):
            self.insert('', 'end', values=(domain,))
            self.domains.add(domain)

    def init(self):
        self.pack(fill='both', expand=True)

        self.bind('<<selfviewSelect>>', self.item_select)
        self.bind('<Delete>', self.delete_selected_items)

#
# root = tk.Tk()
# ws = WhiteListTable(root)
# ws.init()
# root.mainloop()

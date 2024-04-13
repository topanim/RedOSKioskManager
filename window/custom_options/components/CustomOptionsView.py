import tkinter as tk

from window.custom_options.components.Option import Option


class CustomOptionsView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.options = []

    def get_options(self):
        return [option.get() for option in self.options if option.get().is_valid()]

    def on_option_delete(self, option):
        self.options.remove(option)

    def init(self):
        self.pack()
        button = tk.Button(self, text="add option", command=self.add_option)
        button.pack()

        # TODO: DEBUG Option
        button2 = tk.Button(self, text="print options", command=lambda: print(self.get_options()))
        button2.pack()

    def add_option(self):
        option = Option(self, self.on_option_delete)
        self.options.append(option)
        option.init()

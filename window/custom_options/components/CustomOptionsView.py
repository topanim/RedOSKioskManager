import tkinter as tk
from typing import List

from json import loads, dumps

from window.custom_options.components.Option import Option
from window.custom_options.models.OptionDataState import OptionDataState, OptionData


class CustomOptionsView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__options = []

    def get_options(self):
        return [o for option in self.__options if (o := option.get()).is_valid()]

    def on_option_delete(self, option):
        self.__options.remove(option)

    def save_options(self):
        with open('window/custom_options/config/config.json', 'w') as f:
            f.write(dumps(self.get_options()))

    def load_options(self):
        with open('window/custom_options/config/config.json', 'r') as f:
            try:
                options = loads(f.read(), List[OptionData])
            except:
                options = []

        self.clear_options()
        for option in options:
            self.add_option(OptionDataState.from_option_data(option))

        if empty_count := (4 - len(options)):
            for _ in range(empty_count):
                self.add_option()

    # TODO: It was good feature...
    # def import_options(self):
    #     file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    #     if file_path:
    #         with open(file_path, 'r') as f:
    #             try:
    #                 options = loads(f.read(), List[OptionData])
    #                 self.load_options(options)
    #             except:
    #                 messagebox.showerror("Ошибка", "Неверный формат json")

    # def load_options(self, options: List[OptionData]):
    #     self.clear_options()
    #     for option in options:
    #         self.add_option(OptionDataState.from_option_data(option))

    def clear_options(self):
        for option in self.__options:
            option.destroy()

    def init(self):
        self.pack()
        add_option = tk.Button(self, text="add option", command=self.add_option)
        add_option.pack()

        save = tk.Button(self, text="save", command=self.save_options)
        return self


        # TODO: DEBUG Option
        # button2 = tk.Button(self, text="print options", command=lambda: print(self.get_options()))
        # button2.pack()

        # TODO: DEBUG Option
        # button3 = tk.Button(self, text="print dumped options", command=lambda: print(dumps(self.get_options())))
        # button3.pack()

        self.load_options()
        save.pack(side=tk.BOTTOM)


    def add_option(self, ods: OptionDataState = None):
        option = Option(self, self.on_option_delete, ods)
        self.__options.append(option)
        option.init()


root = tk.Tk()
CustomOptionsView(root).init()
root.mainloop()

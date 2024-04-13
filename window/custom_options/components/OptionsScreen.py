import tkinter as tk
from dataclasses import asdict
from json import loads, dumps
from tkinter import ttk

from window.custom_options.components.OptionComponent import Option
from window.custom_options.models.OptionDataState import OptionDataState, OptionData


class OptionsScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, pady=16)
        self.options = []

    def get_options(self):
        return list(filter(lambda it: it.is_valid(), map(lambda x: x.get(), self.options)))

    def on_option_delete(self, option):
        self.options.remove(option)

    def save_options(self):
        with open('window/custom_options/config/config.json', 'w', encoding='utf-8') as f:
            f.write(dumps([asdict(obj) for obj in self.get_options()], ensure_ascii=False))

    def load_options(self):
        with open('window/custom_options/config/config.json', 'r', encoding='utf-8') as f:
            try:
                options = [OptionData(**obj) for obj in loads(f.read())]
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
        for option in self.options:
            option.destroy()

    def init(self):
        self.pack()

        add_option = ttk.Button(self, text="Добавить свойство", style="TButton", command=self.add_option)
        add_option.pack(pady=(0, 16))

        save = ttk.Button(self, text="Сохранить", style="TButton", command=self.save_options)

        # TODO: DEBUG Option
        # button2 = tk.Button(self, text="print options", command=lambda: print(self.get_options()))
        # button2.pack()

        # TODO: DEBUG Option
        # button3 = tk.Button(self, text="print dumped options", command=lambda: print(dumps(self.get_options())))
        # button3.pack()

        self.load_options()
        save.pack(side=tk.BOTTOM, anchor="se", padx=16, pady=16)
        return self

    def add_option(self, ods: OptionDataState = None):
        option = Option(self, self.on_option_delete, ods)
        self.options.append(option)
        option.init()

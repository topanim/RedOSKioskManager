
import tkinter as tk
from tkinter import ttk
from typing import Callable

from window.custom_options.models.OptionData import OptionData
from window.custom_options.static.types import Types


class Option(tk.Frame):
    def __init__(self, master=None, on_destroy: Callable[[tk.Frame], None] = None):
        super().__init__(master)
        self.master_on_destroy = on_destroy
        self.__option = OptionData()

    def get(self):
        return OptionData(
            flag=self.__option.flag.get(),
            desc=self.__option.key.get(),
            type=self.__option.type.get()
        )

    def __on_destroy(self):
        self.master_on_destroy(self)
        self.destroy()

    def init(self):
        self.pack()
        flag = tk.Entry(self, textvariable=self.__option.flag)
        flag.pack(side=tk.LEFT)

        key = tk.Entry(self, textvariable=self.__option.desc)
        key.pack(side=tk.LEFT)

        option_type = ttk.Combobox(self, textvariable=self.__option.type, values=Types.list())
        option_type.pack(side=tk.LEFT)

        button = tk.Button(self, text="::", command=self.__on_destroy)
        button.pack()

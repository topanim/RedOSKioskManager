
import tkinter as tk
from tkinter import ttk
from typing import Callable

from window.custom_options.models.OptionDataState import OptionDataState, OptionData
from window.custom_options.static.types import Types


class Option(tk.Frame):
    def __init__(
            self,
            master=None,
            on_destroy: Callable[[tk.Frame], None] = None,
            ods: OptionDataState = None
    ):
        super().__init__(master)

        self.master_on_destroy = on_destroy
        if ods is None:
            self.__option_state = OptionDataState()
        else:
            self.__option_state = ods

    def get(self) -> OptionData:
        return self.__option_state.to_option_data()

    def __on_destroy(self):
        self.master_on_destroy(self)
        self.destroy()

    def init(self):
        self.pack(padx=16)
        flag = tk.Entry(self, textvariable=self.__option_state.flag)
        flag.pack(side=tk.LEFT)

        key = tk.Entry(self, textvariable=self.__option_state.desc)
        key.pack(side=tk.LEFT)

        option_type = ttk.Combobox(self, textvariable=self.__option_state.type, values=Types.list())
        option_type.pack(side=tk.LEFT)

        button = tk.Button(self, text="Удалить", command=self.__on_destroy)
        button.pack()

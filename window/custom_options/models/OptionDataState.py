from dataclasses import dataclass, field

import tkinter as tk

from window.custom_options.static.types import Types
from window.custom_options.utils.is_not_empty import is_not_empty


@dataclass
class OptionData:
    flag: str = ""
    name: str = ""
    desc: str = ""
    type: str = ""

    def is_valid(self):
        return all([
            (self.flag.startswith("-") and len(self.flag) == 2)
            or self.flag.startswith("--")
            and self.flag.count(" ") == 0
            and is_not_empty(self.flag.replace('-', '')),
            is_not_empty(self.name),
            is_not_empty(self.desc),
            self.type in Types.list()
        ])


@dataclass
class OptionDataState:
    name: tk.StringVar = field(default_factory=tk.StringVar)
    flag: tk.StringVar = field(default_factory=tk.StringVar)
    desc: tk.StringVar = field(default_factory=tk.StringVar)
    type: tk.StringVar = field(default_factory=tk.StringVar)

    @staticmethod
    def from_option_data(od: OptionData):
        return OptionDataState(
            flag=tk.StringVar(value=od.flag),
            name=tk.StringVar(value=od.name),
            desc=tk.StringVar(value=od.desc),
            type=tk.StringVar(value=od.type)
        )

    def to_option_data(self):
        return OptionData(
            flag=self.flag.get(),
            name=self.name.get(),
            desc=self.desc.get(),
            type=self.type.get()
        )

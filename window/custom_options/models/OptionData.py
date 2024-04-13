from dataclasses import dataclass, field

import tkinter as tk

from window.custom_options.static.types import Types
from window.custom_options.utils.is_not_empty import is_not_empty


@dataclass
class OptionData:
    flag: tk.StringVar = field(default_factory=tk.StringVar)
    desc: tk.StringVar = field(default_factory=tk.StringVar)
    type: tk.StringVar = field(default_factory=tk.StringVar)

    def is_valid(self):
        return all([
            (self.flag.startswith("-") and len(self.flag) == 2)
            or self.flag.startswith("--")
            and self.flag.count(" ") == 0
            and is_not_empty(self.flag.replace('-', '')),
            is_not_empty(self.desc),
            self.type in Types.list()
        ])


from dataclasses import dataclass
from tkinter import *
from tkinter import ttk


@dataclass
class ParamsCommand:
    prefix: str
    name: str
    desc: str
    typeEnter: ttk.Checkbutton or ttk.Entry
    values: str or bool or int = None

from dataclasses import dataclass
from tkinter import *


@dataclass
class ParamsCommand:
    prefix: str
    name: str
    typeEnter: Checkbutton or Entry
    values: str or bool or int = None

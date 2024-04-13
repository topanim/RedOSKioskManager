import dataclasses
from tkinter import *

@dataclasses.dataclass
class ParamsCommand:
    prefix: str
    name: str
    typeEnter: Checkbutton or Entry
    values: str or bool or int = None


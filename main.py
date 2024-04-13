from tkinter import *
from tkinter import ttk

import setting
import window.custom_options.components.CustomOptionsView
import window.kiosk

class App:
    def __init__(self):
        root = Tk()
        root.title("Эксперт киоска")
        # root.geometry("450x350")
        root.resizable(False, False)
        self.root = root
        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)

    def make_window(self, win_name: str, frame: Frame) -> ttk.Frame:
        self.notebook.add(frame, text=win_name)
        return frame

    def start(self):
        self.make_window('Киоск', window.kiosk.Window(self.root, self.notebook).create_kiosk())
        self.make_window('Конфигурирование', window.custom_options.components.CustomOptionsView.CustomOptionsView().init())

        self.root.mainloop()


App().start()

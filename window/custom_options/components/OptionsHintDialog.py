import tkinter as tk

from res.strings import options_hint


class OptionsHintDialog(tk.Toplevel):
    def __init__(
            self,
            master=None
    ):
        super().__init__(master, pady=8, padx=8)

    def init(self):
        label_title = tk.Label(self, text="Подсказка")
        label_title.pack()

        label_description = tk.Label(self, text=options_hint, wraplength=300, justify="left")
        label_description.pack()

        ok_button = tk.Button(self, text="OK", command=self.destroy)
        ok_button.pack(side=tk.BOTTOM)

        self.transient()
        self.grab_set()
        self.resizable(False, False)

        self.update_idletasks()
        self.geometry("370x{}".format(self.winfo_reqheight()))
        self.master.wait_window(self)

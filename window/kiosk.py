import json
import os
import subprocess
import tkinter
from tkinter import *
from tkinter import ttk

import obj
import setting
from window.custom_options.components.OptionsHintDialog import OptionsHintDialog
from window.custom_options.models.OptionDataState import OptionData
import tkinter.filedialog

class Window:
    def __init__(self, root, main_note: ttk.Notebook):

        self.command_params = []

        with open('window/custom_options/config/config.json', 'r', encoding='utf-8') as f:
            params = json.loads(f.read())
            for param in params:
                option = OptionData(**param)
                self.command_params.append(
                    obj.ParamsCommand(
                        option.flag,
                        option.name,
                        option.desc,
                        Entry if option.type == 'entry' else Checkbutton
                    )
                )

        self.root = root
        self.notebook = main_note



    def create_kiosk(self) -> tkinter.Frame:

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="white", background="white")
        style.configure('TButton', foreground='black', background=setting.BG_COLOR)
        style.configure('TEntry', foreground='black', background=setting.BG_COLOR)

        frame = tkinter.Frame(self.notebook)
        frame.config(bg=setting.BG_COLOR)
        frame.pack(fill=BOTH, expand=True)

        app_frame = tkinter.Frame(frame)
        app_frame.config(bg=setting.BG_COLOR)

        Label(app_frame, text='Приложения', bg=setting.BG_COLOR).pack(side=LEFT, padx=16)

        frame_with_btn = tkinter.Frame(app_frame)
        frame_with_btn.config(bg=setting.BG_COLOR)

        self.app_name = ttk.Combobox(frame_with_btn, width=24)
        self.app_name.pack(side=RIGHT, padx=16)

        frame_with_btn2 = tkinter.Frame(app_frame)
        frame_with_btn2.config(bg=setting.BG_COLOR)

        ttk.Button(frame_with_btn2, text='Выбрать', command=lambda: self.window_select_app(self.app_name)).pack(
            side=RIGHT, padx=8)

        user_frame = tkinter.Frame(frame)
        user_frame.config(bg=setting.BG_COLOR)

        Label(user_frame, text='Пользователь', bg=setting.BG_COLOR).pack(side=LEFT, padx=16)

        self.username = ttk.Combobox(user_frame, values=self.get_users(), width=24)
        self.username.pack(side=RIGHT, padx=16, pady=(8, 16))

        app_frame.pack(fill=BOTH, pady=(16, 4))
        frame_with_btn.pack(fill=BOTH)
        frame_with_btn2.pack(fill=BOTH, pady=(4, 0), padx=8)
        user_frame.pack(fill=BOTH)

        for param_command in self.command_params:
            var = self.make_frame(param_command, frame)
            param_command.values = var

        ttk.Button(frame, text='Содзать киоск', command=self.command_kiosk_on).pack(pady=(16, 3))
        ttk.Button(frame, text='Отключить киоск', command=self.command_kiosk_off).pack(pady=3)
        ttk.Button(frame, text='Создать файл конфигурирования', command=self.create_import_params).pack(pady=3)

        return frame

    def make_frame(self, param: obj.ParamsCommand, main_frame: Frame):
        frame_down_level = tkinter.Frame(main_frame, width=5)
        frame_down_level.config(bg=setting.BG_COLOR)

        Label(frame_down_level, text=param.name, bg=setting.BG_COLOR).pack(side=LEFT, padx=16)
        input_entry = ttk.Entry(frame_down_level, style="TEntry", width=20)
        var = input_entry
        if param.typeEnter == Checkbutton:
            var = IntVar()
            input_entry = Checkbutton(frame_down_level, background=setting.BG_COLOR, variable=var, onvalue=1, offvalue=0)

        hint = ttk.Button(frame_down_level, text="?", style="TButton", width=3,
                              command=lambda: OptionsHintDialog(param, main_frame).init())
        hint.pack(side=RIGHT, padx=(0, 16))
        input_entry.pack(side=RIGHT, padx=8)
        frame_down_level.pack(fill=BOTH, pady=(0, 8))
        return var

    def window_select_app(self, combobox: ttk.Combobox):
        windows = Toplevel(self.root)

        app_name = Listbox(windows, selectmode="multiple", exportselection=0)
        self.create_app_name(app_name)
        app_name.pack()

        app_name.bind("<<ListboxSelect>>", lambda _: self.update_combobox(app_name, combobox))

    def create_app_name(self, app_name_obj: Listbox):

        if setting.DEBUG:
            progs_list = ['1', 'sadfasdf', 'xcbzxzcb']
        else:
            progs = subprocess.check_output(['less', '/usr/share/applications']).decode('utf-8').split(" ")
            progs_list = list(filter(lambda x: "\n" in x, progs))
            progs_list = list(map(lambda x: x.split("\n")[0], progs_list))[3:]
            progs_list = list(map(lambda x: x.replace('.desktop', ''), progs_list))

        for i in progs_list:
            app_name_obj.insert(END, i)

    def update_combobox(self, listbox: Listbox, combobox: ttk.Combobox):
        # Get selected values from the Listbox widget
        selected_values = [listbox.get(idx) for idx in listbox.curselection()]

        # Update the combobox with the selected values
        combobox.configure(width=40, height=7)
        combobox.set(", ".join(selected_values))

    def get_users(self):
        if setting.DEBUG:
            proc_lists = ['sdfg', 'df123123']
        else:
            proc = subprocess.check_output(["less", "/etc/passwd"]).decode('utf-8').split('\n')
            proc_lists = list(map(lambda x: x.split(":"), proc))
            proc_lists = list(map(lambda x: x[0], proc_lists))
        return proc_lists

    def command_kiosk_on(self):
        cmd_parm = []
        if len(self.app_name.get()) > 0:
            cmd = f'-a {self.app_name.get()}'
            cmd_parm.append(cmd)

        if len(self.username.get()) > 0:
            cmd = f'-u {self.username.get()}'
            cmd_parm.append(cmd)

        for i in self.command_params:
            if i.typeEnter == Checkbutton and i.values.get() == 1:
                cmd_parm.append(i.prefix)
            if i.typeEnter != Checkbutton and (str(i.values.get()) != "0" and len(str(i.values.get())) != 0):
                cmd_parm.append(f"{i.prefix} {i.values.get()}")
        os.system(f'sudo kiosk-mode-on {" ".join(cmd_parm)}')

    def command_kiosk_off(self):
        cmd_parm = []

        if len(self.username.get()) > 0:
            cmd = f'-u {self.username.get()}'
            cmd_parm.append(cmd)

        os.system(f'sudo kiosk-mode-off {" ".join(cmd_parm)}')

    def make_window(self, win_name: str, frame: Frame) -> ttk.Frame:
        self.notebook.add(frame, text=win_name)
        return frame

    def create_import_params(self):
        def save_file():
            file = tkinter.filedialog.asksaveasfile(initialfile='kiosk-mode-on.sh',
                          defaultextension=".sh", filetypes=[("All Files", "*.*"), ("Text Documents", "*.sh")])

            file.write("\n".join(create_config()))
            file.close()  # `()` was missing.

        def create_config():
            cmd_parm = []
            sh_cmd = []
            if is_create_user.get() == 1:
                sh_cmd.append(f"sudo useradd {self.username.get()}")

            if len(self.app_name.get()) > 0:
                cmd = f'-a {self.app_name.get()}'
                cmd_parm.append(cmd)

            if len(self.username.get()) > 0:
                cmd = f'-u {self.username.get()}'
                cmd_parm.append(cmd)

            if is_use_keys.get() == 1:
                for i in self.command_params:
                    if i.typeEnter == Checkbutton and i.values.get() == 1:
                        cmd_parm.append(i.prefix)
                    if i.typeEnter != Checkbutton and (str(i.values.get()) != "0" and len(str(i.values.get())) != 0):
                        cmd_parm.append(f"{i.prefix} {i.values.get()}")
            sh_cmd.append(f"sudo kiosk-mode-on {' '.join(cmd_parm)}")
            return sh_cmd


        windows = Toplevel(self.root)
        windows.geometry("300x140")

        create_user = obj.ParamsCommand('', 'Создавать пользователя?', 'Создает нового пользователя в системе. Имя нового пользователя указывается в `Пользователь`', Checkbutton)
        use_keys = obj.ParamsCommand('', 'Импортирова ключи?', 'Импортирует ключи команды при создании sh файла', Checkbutton)
        is_create_user = self.make_frame(create_user, windows)
        is_use_keys = self.make_frame(use_keys, windows)
        btn_create = Button(windows, text="Создать", command=save_file)
        btn_create.pack(pady=16)


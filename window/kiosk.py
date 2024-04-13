import dataclasses
import json
import os
import subprocess
import tkinter
from tkinter import *
from tkinter import ttk
import obj
from window.custom_options.components.OptionsHintDialog import OptionsHintDialog
from window.custom_options.models.OptionDataState import OptionData

import setting


class Window:
    def __init__(self, root, main_note: ttk.Notebook):

        self.command_params = []

        with open('window/custom_options/config/config.json') as f:
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
        frame = tkinter.Frame(self.notebook)
        frame.config(bg='white')
        frame.pack(fill=BOTH, expand=True)

        app_frame = tkinter.Frame(frame)
        app_frame.config(bg='white')

        Label(app_frame, text='Приложения').pack(side=LEFT, padx=16)

        frame_with_btn = tkinter.Frame(app_frame)
        frame_with_btn.config(bg='white')

        self.app_name = ttk.Combobox(frame_with_btn, state="readonly", width=25)
        self.app_name.pack(side=RIGHT, padx=5)


        frame_with_btn2 = tkinter.Frame(app_frame)
        frame_with_btn2.config(bg='white')

        Button(frame_with_btn2, text='Выбрать', command=lambda: self.window_select_app(self.app_name)).pack(side=RIGHT)

        user_frame = ttk.Frame(frame)
        Label(user_frame, text='Пользователь').pack(side=LEFT, padx=16)

        self.username = ttk.Combobox(user_frame, values=self.get_users(), width=22)
        self.username.pack(side=RIGHT, padx=5)

        app_frame.pack(fill=BOTH, pady=(16, 4))
        frame_with_btn.pack(fill=BOTH)
        frame_with_btn2.pack(fill=BOTH, pady=(4, 0), padx=8)
        user_frame.pack(fill=BOTH)

        for param_command in self.command_params:
            var = self.make_frame(param_command, frame)
            param_command.values = var

        Button(frame, text='Содзать киоск', command=self.command_kiosk_on).pack(pady=(16, 3))
        Button(frame, text='Отключить киоск', command=self.command_kiosk_off).pack(pady=3)
        Button(frame, text='Создать файл конфигурирования', command=self.create_import_params).pack(pady=3)

        return frame

    def make_frame(self, param: obj.ParamsCommand, main_frame: Frame):
        frame_down_level = ttk.Frame(main_frame, width=5)
        Label(frame_down_level, text=param.name).pack(side=LEFT, padx=16)
        input_entry = param.typeEnter(frame_down_level, width=23)
        var = input_entry
        if param.typeEnter == Checkbutton:
            var = IntVar()
            input_entry = param.typeEnter(frame_down_level, variable=var, onvalue=1, offvalue=0)

        hint = tkinter.Button(frame_down_level, text="?",
                              command=lambda: OptionsHintDialog(param, main_frame).init())
        hint.pack(side=RIGHT)
        input_entry.pack(side=RIGHT, padx=8)
        frame_down_level.pack(fill=BOTH)
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
        windows.geometry("250x125")
        is_create_user = self.make_frame('Создавать пользователя?', Checkbutton, windows)
        is_use_keys = self.make_frame('Использовать ключи?', Checkbutton, windows)
        btn_create = Button(windows, text="Создать", command=save_file)
        btn_create.pack(pady=16)


import dataclasses
import os
import subprocess
import tkinter
from tkinter import *
from tkinter import ttk
import obj

debug_windows = True

class Window:
    def __init__(self, root, main_note: ttk.Notebook):
        self.root = root
        self.notebook = main_note
        self.command_params = [obj.ParamsCommand('--timelock', 'Время до блокировки', Entry),
                               obj.ParamsCommand('--blockbtn', 'Отображение кнопки блокирования экрана', Checkbutton),
                               obj.ParamsCommand('--autohide', 'Автоматического скрытия главной панели', Checkbutton),
                               obj.ParamsCommand('--quiet', 'Подавление вывода на экран', Checkbutton)]

    def create_kiosk(self) -> tkinter.Frame:
        frame = ttk.Frame(self.notebook)
        frame.pack(fill=BOTH, expand=True)

        app_frame = ttk.Frame(frame)

        Label(app_frame, text='Приложения').pack(side=LEFT, padx=16)

        frame_with_btn = ttk.Frame(app_frame)

        self.app_name = ttk.Combobox(frame_with_btn, state="readonly", width=25)
        self.app_name.pack(side=LEFT, padx=5)

        Button(frame_with_btn, text='Выбрать', command=lambda: self.window_select_app(self.app_name)).pack(side=RIGHT)

        user_frame = ttk.Frame(frame)
        Label(user_frame, text='Пользователь').pack(side=LEFT, padx=16)

        self.username = ttk.Combobox(user_frame, values=self.get_users(), width=22)
        self.username.pack(side=RIGHT, padx=5)

        app_frame.pack(fill=BOTH)
        frame_with_btn.pack(fill=BOTH)
        user_frame.pack(fill=BOTH)

        for i in self.command_params:
            var = self.make_frame(i.name, i.typeEnter, frame)
            i.values = var

        Button(frame, text='Содзать киоск', command=self.command_kiosk_on).pack(pady=(16, 3))
        Button(frame, text='Отключить киоск', command=self.command_kiosk_off).pack(pady=3)
        Button(frame, text='Создать файл конфигурирования', command=self.create_import_params).pack(pady=3)

        return frame

    def make_frame(self, label_text: str, entry_type, main_frame: Frame):
        frame_down_level = ttk.Frame(main_frame, width=5)
        Label(frame_down_level, text=label_text).pack(side=LEFT, padx=16)
        input_entry = entry_type(frame_down_level, width=23)
        var = input_entry
        if entry_type == Checkbutton:
            var = IntVar()
            input_entry = entry_type(frame_down_level, variable=var, onvalue=1, offvalue=0)
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

        if debug_windows:
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
        if debug_windows:
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
        windows = Toplevel(self.root)
        windows.geometry("250x125")
        is_create_user = self.make_frame('Создавать пользователя?', Checkbutton, windows)
        is_use_keys = self.make_frame('Использовать ключи?', Checkbutton, windows)
        btn_create = Button(windows, text="Создать")
        btn_create.pack(pady=16)

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

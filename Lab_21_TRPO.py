import sqlite3
import tkinter as tk
from tkinter import ttk, Menu


class Main_Window():
    material_menu: Menu

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("700x550")
        self.root.title("Материальный склад")

        self.main_menu = tk.Menu()

        self.file_menu = tk.Menu(tearoff=0)  # подменю
        self.ref_menu = tk.Menu(tearoff=0)  # подменю
        self.material_menu = tk.Menu(tearoff=0)  # подменю
        self.otch_menu = tk.Menu(tearoff=0)  # подменю
        self.help_menu = tk.Menu(tearoff=0)  # подменю

        self.file_menu.add_command(label="Выход", command=quit)

        self.ref_menu.add_command(label="Проставщики", command=self.open_win_provider)
        self.ref_menu.add_command(label="Типы", command=self.open_win_type)

        self.material_menu.add_command(label='Поступление материалов',command=self.open_win_receipt)
        self.material_menu.add_command(label='Список материалов',command=self.open_win_list)
        self.material_menu.add_command(label='Передача в производство',command=self.open_win_per)
        self.material_menu.add_command(label='Списание материалов',command=self.open_win_write_off)

        self.otch_menu.add_command(label="Отчет по поступлению")
        self.otch_menu.add_command(label="Отчет по передаче в производство")
        self.otch_menu.add_command(label="Отчет по списанию материалов")

        self.help_menu.add_command(label="Руководство пользователя")
        self.help_menu.add_command(label="О программе")

        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
        self.main_menu.add_cascade(label="Справочники", menu=self.ref_menu)
        self.main_menu.add_cascade(label="Материалы", menu=self.material_menu)
        self.main_menu.add_cascade(label="Отчеты", menu=self.otch_menu)
        self.main_menu.add_cascade(label="Справка", menu=self.help_menu)

        # привязываем меню к созданному окну
        self.root.config(menu=self.main_menu)

    def open_win_provider(self):
        self.root.withdraw()  # скрыть окно
        Provider_Window()

    def open_win_type(self):
        self.root.withdraw()  # скрыть окно
        type_Window()

    def open_win_receipt(self):
        self.root.withdraw()  # скрыть окно
        receipts_Window()

    def open_win_list(self):
        self.root.withdraw()  # скрыть окно
        list_Window()

    def open_win_per(self):
        self.root.withdraw()  # скрыть окно
        per_Window()

    def open_win_write_off(self):
        self.root.withdraw()  # скрыть окно
        write_off_Window()

class Provider_Window():
    '''Окно Поставщики'''

    def __init__(self):
        self.root2 = tk.Tk()
        self.root2.geometry("800x500")
        self.root2.title("Материальный склад/Поставщики")
        self.root2.protocol('WM_DELETE_WINDOW', lambda: self.quit_win_provider())  # перехват кнопки Х
        self.main_view = win
        self.db = db

        # фреймы
        self.table_frame = tk.Frame(self.root2, bg='green')
        self.add_edit_frame = tk.Frame(self.root2, bg='red')

        self.table_frame.place(relx=0, rely=0, relheight=1, relwidth=0.6)
        self.add_edit_frame.place(relx=0.6, rely=0, relheight=1, relwidth=0.4)

        # таблица
        self.table_pr = ttk.Treeview(self.table_frame, columns=('name_provider', 'contact_person', 'phone_number'),
                                     height=15, show='headings')
        self.table_pr.column("name_provider", width=150, anchor=tk.NW)
        self.table_pr.column("contact_person", width=200, anchor=tk.NW)
        self.table_pr.column("phone_number", width=120, anchor=tk.CENTER)

        self.table_pr.heading("name_provider", text='Наименование')
        self.table_pr.heading("contact_person", text='Контактное лицо')
        self.table_pr.heading("phone_number", text='Номер телефона')

        # Полоса прокрутки
        self.scroll_bar = ttk.Scrollbar(self.table_frame)
        self.table_pr['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_pr.place(relx=0, rely=0, relheight=0.9, relwidth=0.97)

        # поле ввода и кнопка для поиска
        self.esearch = ttk.Entry(self.table_frame)
        self.esearch.place(relx=0.02, rely=0.92, relheight=0.05, relwidth=0.7)

        self.butsearch = tk.Button(self.table_frame, text="Найти")
        self.butsearch.place(relx=0.74, rely=0.92, relheight=0.05, relwidth=0.2)

        # поля для ввода
        self.lname = tk.Label(self.add_edit_frame, text="Наименование")
        self.lname.place(relx=0.04, rely=0.02, relheight=0.05, relwidth=0.4)
        self.ename = ttk.Entry(self.add_edit_frame)
        self.ename.place(relx=0.45, rely=0.02, relheight=0.05, relwidth=0.5)

        self.lcontact = tk.Label(self.add_edit_frame, text="Контактное лицо")
        self.lcontact.place(relx=0.04, rely=0.12, relheight=0.05, relwidth=0.4)
        self.econtact = ttk.Entry(self.add_edit_frame)
        self.econtact.place(relx=0.45, rely=0.12, relheight=0.05, relwidth=0.5)

        self.lphone = tk.Label(self.add_edit_frame, text="Номер телефона")
        self.lphone.place(relx=0.04, rely=0.22, relheight=0.05, relwidth=0.4)

        # валидация номера телефона для поля ввода
        self.ephone = ttk.Entry(self.add_edit_frame)
        self.ephone.place(relx=0.45, rely=0.22, relheight=0.05, relwidth=0.5)
        self.ephone.insert(0, "+375")

        # кнопки
        self.butadd = tk.Button(self.add_edit_frame, text="Добавить запись")
        self.butadd.place(relx=0.1, rely=0.33, relheight=0.07, relwidth=0.8)

        self.butdel = tk.Button(self.add_edit_frame, text="Удалить запись")
        self.butdel.place(relx=0.1, rely=0.44, relheight=0.07, relwidth=0.8)

        self.buted = tk.Button(self.add_edit_frame, text="Редактировать запись")
        self.buted.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

        self.butsave = tk.Button(self.add_edit_frame, text="Сохранить изменения")
        self.butsave.place(relx=0.1, rely=0.66, relheight=0.07, relwidth=0.8)

        self.butquit = tk.Button(self.add_edit_frame, text="Закрыть")
        self.butquit.place(relx=0.1, rely=0.77, relheight=0.07, relwidth=0.8)

    def quit_win_provider(self):
        self.root2.destroy()
        self.main_view.root.deiconify()

class type_Window():
    '''Окно Поставщики'''

    def __init__(self):
        self.root3 = tk.Tk()
        self.root3.geometry("800x500")
        self.root3.title("Материальный склад/Типы материалов")
        self.root3.protocol('WM_DELETE_WINDOW', lambda: self.quit_win_type())  # перехват кнопки Х
        self.main_view = win
        self.db = db

        # фреймы
        self.table_frame = tk.Frame(self.root3, bg='green')
        self.add_edit_frame = tk.Frame(self.root3, bg='red')

        self.table_frame.place(relx=0, rely=0, relheight=1, relwidth=0.6)
        self.add_edit_frame.place(relx=0.6, rely=0, relheight=1, relwidth=0.4)

        # таблица
        self.table_pr = ttk.Treeview(self.table_frame, columns=('name_type', 'contact_person', 'phone_number'),
                                     height=15, show='headings')
        self.table_pr.column("name_type", width=150, anchor=tk.NW)
        self.table_pr.column("contact_person", width=200, anchor=tk.NW)
        self.table_pr.column("phone_number", width=120, anchor=tk.CENTER)

        self.table_pr.heading("name_type", text='Наименование')
        self.table_pr.heading("contact_person", text='Контактное лицо')
        self.table_pr.heading("phone_number", text='Номер телефона')

        # Полоса прокрутки
        self.scroll_bar = ttk.Scrollbar(self.table_frame)
        self.table_pr['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_pr.place(relx=0, rely=0, relheight=0.9, relwidth=0.97)

        # поле ввода и кнопка для поиска
        self.esearch = ttk.Entry(self.table_frame)
        self.esearch.place(relx=0.02, rely=0.92, relheight=0.05, relwidth=0.7)

        self.butsearch = tk.Button(self.table_frame, text="Найти")
        self.butsearch.place(relx=0.74, rely=0.92, relheight=0.05, relwidth=0.2)

        # поля для ввода
        self.lname = tk.Label(self.add_edit_frame, text="Наименование")
        self.lname.place(relx=0.04, rely=0.02, relheight=0.05, relwidth=0.4)
        self.ename = ttk.Entry(self.add_edit_frame)
        self.ename.place(relx=0.45, rely=0.02, relheight=0.05, relwidth=0.5)

        self.lcontact = tk.Label(self.add_edit_frame, text="Контактное лицо")
        self.lcontact.place(relx=0.04, rely=0.12, relheight=0.05, relwidth=0.4)
        self.econtact = ttk.Entry(self.add_edit_frame)
        self.econtact.place(relx=0.45, rely=0.12, relheight=0.05, relwidth=0.5)

        self.lphone = tk.Label(self.add_edit_frame, text="Номер телефона")
        self.lphone.place(relx=0.04, rely=0.22, relheight=0.05, relwidth=0.4)

        # валидация номера телефона для поля ввода
        self.ephone = ttk.Entry(self.add_edit_frame)
        self.ephone.place(relx=0.45, rely=0.22, relheight=0.05, relwidth=0.5)
        self.ephone.insert(0, "+375")

        # кнопки
        self.butadd = tk.Button(self.add_edit_frame, text="Добавить запись")
        self.butadd.place(relx=0.1, rely=0.33, relheight=0.07, relwidth=0.8)

        self.butdel = tk.Button(self.add_edit_frame, text="Удалить запись")
        self.butdel.place(relx=0.1, rely=0.44, relheight=0.07, relwidth=0.8)

        self.buted = tk.Button(self.add_edit_frame, text="Редактировать запись")
        self.buted.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

        self.butsave = tk.Button(self.add_edit_frame, text="Сохранить изменения")
        self.butsave.place(relx=0.1, rely=0.66, relheight=0.07, relwidth=0.8)

        self.butquit = tk.Button(self.add_edit_frame, text="Закрыть")
        self.butquit.place(relx=0.1, rely=0.77, relheight=0.07, relwidth=0.8)

    def quit_win_type(self):
        self.root3.destroy()
        self.main_view.root.deiconify()

class receipts_Window():
    def __init__(self):
        self.root4 = tk.Tk()
        self.root4.geometry("800x500")
        self.root4.title("Материальный склад/Поступление материалов")
        self.root4.protocol('WM_DELETE_WINDOW', lambda: self.quit_win_receipt())  # перехват кнопки Х
        self.main_view = win
        self.db = db

        # фреймы
        self.table_frame = tk.Frame(self.root4, bg='green')
        self.add_edit_frame = tk.Frame(self.root4, bg='red')

        self.table_frame.place(relx=0, rely=0, relheight=1, relwidth=0.6)
        self.add_edit_frame.place(relx=0.6, rely=0, relheight=1, relwidth=0.4)

        # таблица
        self.table_pr = ttk.Treeview(self.table_frame, columns=('name_type', 'contact_person', 'phone_number'),
                                     height=15, show='headings')
        self.table_pr.column("name_type", width=150, anchor=tk.NW)
        self.table_pr.column("contact_person", width=200, anchor=tk.NW)
        self.table_pr.column("phone_number", width=120, anchor=tk.CENTER)

        self.table_pr.heading("name_type", text='Наименование')
        self.table_pr.heading("contact_person", text='Контактное лицо')
        self.table_pr.heading("phone_number", text='Номер телефона')

        # Полоса прокрутки
        self.scroll_bar = ttk.Scrollbar(self.table_frame)
        self.table_pr['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_pr.place(relx=0, rely=0, relheight=0.9, relwidth=0.97)

        # поле ввода и кнопка для поиска
        self.esearch = ttk.Entry(self.table_frame)
        self.esearch.place(relx=0.02, rely=0.92, relheight=0.05, relwidth=0.7)

        self.butsearch = tk.Button(self.table_frame, text="Найти")
        self.butsearch.place(relx=0.74, rely=0.92, relheight=0.05, relwidth=0.2)

        # поля для ввода
        self.lname = tk.Label(self.add_edit_frame, text="Наименование")
        self.lname.place(relx=0.04, rely=0.02, relheight=0.05, relwidth=0.4)
        self.ename = ttk.Entry(self.add_edit_frame)
        self.ename.place(relx=0.45, rely=0.02, relheight=0.05, relwidth=0.5)

        self.lcontact = tk.Label(self.add_edit_frame, text="Контактное лицо")
        self.lcontact.place(relx=0.04, rely=0.12, relheight=0.05, relwidth=0.4)
        self.econtact = ttk.Entry(self.add_edit_frame)
        self.econtact.place(relx=0.45, rely=0.12, relheight=0.05, relwidth=0.5)

        self.lphone = tk.Label(self.add_edit_frame, text="Номер телефона")
        self.lphone.place(relx=0.04, rely=0.22, relheight=0.05, relwidth=0.4)

        # валидация номера телефона для поля ввода
        self.ephone = ttk.Entry(self.add_edit_frame)
        self.ephone.place(relx=0.45, rely=0.22, relheight=0.05, relwidth=0.5)
        self.ephone.insert(0, "+375")

        # кнопки
        self.butadd = tk.Button(self.add_edit_frame, text="Добавить запись")
        self.butadd.place(relx=0.1, rely=0.33, relheight=0.07, relwidth=0.8)

        self.butdel = tk.Button(self.add_edit_frame, text="Удалить запись")
        self.butdel.place(relx=0.1, rely=0.44, relheight=0.07, relwidth=0.8)

        self.buted = tk.Button(self.add_edit_frame, text="Редактировать запись")
        self.buted.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

        self.butsave = tk.Button(self.add_edit_frame, text="Сохранить изменения")
        self.butsave.place(relx=0.1, rely=0.66, relheight=0.07, relwidth=0.8)

        self.butquit = tk.Button(self.add_edit_frame, text="Закрыть")
        self.butquit.place(relx=0.1, rely=0.77, relheight=0.07, relwidth=0.8)

    def quit_win_receipt(self):
        self.root4.destroy()
        self.main_view.root.deiconify()

class list_Window():
    def __init__(self):
        self.root5 = tk.Tk()
        self.root5.geometry("800x500")
        self.root5.title("Материальный склад/Список материалов")
        self.root5.protocol('WM_DELETE_WINDOW', lambda: self.quit_win_list())  # перехват кнопки Х
        self.main_view = win
        self.db = db

        # фреймы
        self.table_frame = tk.Frame(self.root5, bg='green')
        self.add_edit_frame = tk.Frame(self.root5, bg='red')

        self.table_frame.place(relx=0, rely=0, relheight=1, relwidth=0.6)
        self.add_edit_frame.place(relx=0.6, rely=0, relheight=1, relwidth=0.4)

        # таблица
        self.table_pr = ttk.Treeview(self.table_frame, columns=('name_type', 'contact_person', 'phone_number'),
                                     height=15, show='headings')
        self.table_pr.column("name_type", width=150, anchor=tk.NW)
        self.table_pr.column("contact_person", width=200, anchor=tk.NW)
        self.table_pr.column("phone_number", width=120, anchor=tk.CENTER)

        self.table_pr.heading("name_type", text='Наименование')
        self.table_pr.heading("contact_person", text='Контактное лицо')
        self.table_pr.heading("phone_number", text='Номер телефона')

        # Полоса прокрутки
        self.scroll_bar = ttk.Scrollbar(self.table_frame)
        self.table_pr['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_pr.place(relx=0, rely=0, relheight=0.9, relwidth=0.97)

        # поле ввода и кнопка для поиска
        self.esearch = ttk.Entry(self.table_frame)
        self.esearch.place(relx=0.02, rely=0.92, relheight=0.05, relwidth=0.7)

        self.butsearch = tk.Button(self.table_frame, text="Найти")
        self.butsearch.place(relx=0.74, rely=0.92, relheight=0.05, relwidth=0.2)

        # поля для ввода
        self.lname = tk.Label(self.add_edit_frame, text="Наименование")
        self.lname.place(relx=0.04, rely=0.02, relheight=0.05, relwidth=0.4)
        self.ename = ttk.Entry(self.add_edit_frame)
        self.ename.place(relx=0.45, rely=0.02, relheight=0.05, relwidth=0.5)

        self.lcontact = tk.Label(self.add_edit_frame, text="Контактное лицо")
        self.lcontact.place(relx=0.04, rely=0.12, relheight=0.05, relwidth=0.4)
        self.econtact = ttk.Entry(self.add_edit_frame)
        self.econtact.place(relx=0.45, rely=0.12, relheight=0.05, relwidth=0.5)

        self.lphone = tk.Label(self.add_edit_frame, text="Номер телефона")
        self.lphone.place(relx=0.04, rely=0.22, relheight=0.05, relwidth=0.4)

        # валидация номера телефона для поля ввода
        self.ephone = ttk.Entry(self.add_edit_frame)
        self.ephone.place(relx=0.45, rely=0.22, relheight=0.05, relwidth=0.5)
        self.ephone.insert(0, "+375")

        # кнопки
        self.butadd = tk.Button(self.add_edit_frame, text="Добавить запись")
        self.butadd.place(relx=0.1, rely=0.33, relheight=0.07, relwidth=0.8)

        self.butdel = tk.Button(self.add_edit_frame, text="Удалить запись")
        self.butdel.place(relx=0.1, rely=0.44, relheight=0.07, relwidth=0.8)

        self.buted = tk.Button(self.add_edit_frame, text="Редактировать запись")
        self.buted.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

        self.butsave = tk.Button(self.add_edit_frame, text="Сохранить изменения")
        self.butsave.place(relx=0.1, rely=0.66, relheight=0.07, relwidth=0.8)

        self.butquit = tk.Button(self.add_edit_frame, text="Закрыть")
        self.butquit.place(relx=0.1, rely=0.77, relheight=0.07, relwidth=0.8)

    def quit_win_list(self):
        self.root5.destroy()
        self.main_view.root.deiconify()

class write_off_Window():
    def __init__(self):
        self.root7 = tk.Tk()
        self.root7.geometry("800x500")
        self.root7.title("Материальный склад/Списание Материалов")
        self.root7.protocol('WM_DELETE_WINDOW', lambda: self.quit_win_write_off())  # перехват кнопки Х
        self.main_view = win
        self.db = db

        # фреймы
        self.table_frame = tk.Frame(self.root7, bg='green')
        self.add_edit_frame = tk.Frame(self.root7, bg='red')

        self.table_frame.place(relx=0, rely=0, relheight=1, relwidth=0.6)
        self.add_edit_frame.place(relx=0.6, rely=0, relheight=1, relwidth=0.4)

        # таблица
        self.table_pr = ttk.Treeview(self.table_frame, columns=('name_type', 'contact_person', 'phone_number'),
                                     height=15, show='headings')
        self.table_pr.column("name_type", width=150, anchor=tk.NW)
        self.table_pr.column("contact_person", width=200, anchor=tk.NW)
        self.table_pr.column("phone_number", width=120, anchor=tk.CENTER)

        self.table_pr.heading("name_type", text='Наименование')
        self.table_pr.heading("contact_person", text='Контактное лицо')
        self.table_pr.heading("phone_number", text='Номер телефона')

        # Полоса прокрутки
        self.scroll_bar = ttk.Scrollbar(self.table_frame)
        self.table_pr['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_pr.place(relx=0, rely=0, relheight=0.9, relwidth=0.97)

        # поле ввода и кнопка для поиска
        self.esearch = ttk.Entry(self.table_frame)
        self.esearch.place(relx=0.02, rely=0.92, relheight=0.05, relwidth=0.7)

        self.butsearch = tk.Button(self.table_frame, text="Найти")
        self.butsearch.place(relx=0.74, rely=0.92, relheight=0.05, relwidth=0.2)

        # поля для ввода
        self.lname = tk.Label(self.add_edit_frame, text="Наименование")
        self.lname.place(relx=0.04, rely=0.02, relheight=0.05, relwidth=0.4)
        self.ename = ttk.Entry(self.add_edit_frame)
        self.ename.place(relx=0.45, rely=0.02, relheight=0.05, relwidth=0.5)

        self.lcontact = tk.Label(self.add_edit_frame, text="Контактное лицо")
        self.lcontact.place(relx=0.04, rely=0.12, relheight=0.05, relwidth=0.4)
        self.econtact = ttk.Entry(self.add_edit_frame)
        self.econtact.place(relx=0.45, rely=0.12, relheight=0.05, relwidth=0.5)

        self.lphone = tk.Label(self.add_edit_frame, text="Номер телефона")
        self.lphone.place(relx=0.04, rely=0.22, relheight=0.05, relwidth=0.4)

        # валидация номера телефона для поля ввода
        self.ephone = ttk.Entry(self.add_edit_frame)
        self.ephone.place(relx=0.45, rely=0.22, relheight=0.05, relwidth=0.5)
        self.ephone.insert(0, "+375")

        # кнопки
        self.butadd = tk.Button(self.add_edit_frame, text="Добавить запись")
        self.butadd.place(relx=0.1, rely=0.33, relheight=0.07, relwidth=0.8)

        self.butdel = tk.Button(self.add_edit_frame, text="Удалить запись")
        self.butdel.place(relx=0.1, rely=0.44, relheight=0.07, relwidth=0.8)

        self.buted = tk.Button(self.add_edit_frame, text="Редактировать запись")
        self.buted.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

        self.butsave = tk.Button(self.add_edit_frame, text="Сохранить изменения")
        self.butsave.place(relx=0.1, rely=0.66, relheight=0.07, relwidth=0.8)

        self.butquit = tk.Button(self.add_edit_frame, text="Закрыть")
        self.butquit.place(relx=0.1, rely=0.77, relheight=0.07, relwidth=0.8)

    def quit_win_write_off(self):
        self.root7.destroy()
        self.main_view.root.deiconify()
class per_Window():
    def __init__(self):
        self.root6 = tk.Tk()
        self.root6.geometry("800x500")
        self.root6.title("Материальный склад/Передача в производство")
        self.root6.protocol('WM_DELETE_WINDOW', lambda: self.quit_win_per())  # перехват кнопки Х
        self.main_view = win
        self.db = db

        # фреймы
        self.table_frame = tk.Frame(self.root6, bg='green')
        self.add_edit_frame = tk.Frame(self.root6, bg='red')

        self.table_frame.place(relx=0, rely=0, relheight=1, relwidth=0.6)
        self.add_edit_frame.place(relx=0.6, rely=0, relheight=1, relwidth=0.4)

        # таблица
        self.table_pr = ttk.Treeview(self.table_frame, columns=('name_type', 'contact_person', 'phone_number'),
                                     height=15, show='headings')
        self.table_pr.column("name_type", width=150, anchor=tk.NW)
        self.table_pr.column("contact_person", width=200, anchor=tk.NW)
        self.table_pr.column("phone_number", width=120, anchor=tk.CENTER)

        self.table_pr.heading("name_type", text='Наименование')
        self.table_pr.heading("contact_person", text='Контактное лицо')
        self.table_pr.heading("phone_number", text='Номер телефона')

        # Полоса прокрутки
        self.scroll_bar = ttk.Scrollbar(self.table_frame)
        self.table_pr['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_pr.place(relx=0, rely=0, relheight=0.9, relwidth=0.97)

        # поле ввода и кнопка для поиска
        self.esearch = ttk.Entry(self.table_frame)
        self.esearch.place(relx=0.02, rely=0.92, relheight=0.05, relwidth=0.7)

        self.butsearch = tk.Button(self.table_frame, text="Найти")
        self.butsearch.place(relx=0.74, rely=0.92, relheight=0.05, relwidth=0.2)

        # поля для ввода
        self.lname = tk.Label(self.add_edit_frame, text="Наименование")
        self.lname.place(relx=0.04, rely=0.02, relheight=0.05, relwidth=0.4)
        self.ename = ttk.Entry(self.add_edit_frame)
        self.ename.place(relx=0.45, rely=0.02, relheight=0.05, relwidth=0.5)

        self.lcontact = tk.Label(self.add_edit_frame, text="Контактное лицо")
        self.lcontact.place(relx=0.04, rely=0.12, relheight=0.05, relwidth=0.4)
        self.econtact = ttk.Entry(self.add_edit_frame)
        self.econtact.place(relx=0.45, rely=0.12, relheight=0.05, relwidth=0.5)

        self.lphone = tk.Label(self.add_edit_frame, text="Номер телефона")
        self.lphone.place(relx=0.04, rely=0.22, relheight=0.05, relwidth=0.4)

        # валидация номера телефона для поля ввода
        self.ephone = ttk.Entry(self.add_edit_frame)
        self.ephone.place(relx=0.45, rely=0.22, relheight=0.05, relwidth=0.5)
        self.ephone.insert(0, "+375")

        # кнопки
        self.butadd = tk.Button(self.add_edit_frame, text="Добавить запись")
        self.butadd.place(relx=0.1, rely=0.33, relheight=0.07, relwidth=0.8)

        self.butdel = tk.Button(self.add_edit_frame, text="Удалить запись")
        self.butdel.place(relx=0.1, rely=0.44, relheight=0.07, relwidth=0.8)

        self.buted = tk.Button(self.add_edit_frame, text="Редактировать запись")
        self.buted.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

        self.butsave = tk.Button(self.add_edit_frame, text="Сохранить изменения")
        self.butsave.place(relx=0.1, rely=0.66, relheight=0.07, relwidth=0.8)

        self.butquit = tk.Button(self.add_edit_frame, text="Закрыть")
        self.butquit.place(relx=0.1, rely=0.77, relheight=0.07, relwidth=0.8)

    def quit_win_per(self):
        self.root6.destroy()
        self.main_view.root.deiconify()
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('material_bd.db')  # установили связь с БД (или создали если ее нет)
        self.c = self.conn.cursor()  # создали курсор
        # таблица Книги
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "material" (
                       "id_material" INTEGER NOT NULL,
                        "id" INTEGER,
                        "name" TEXT NOT NULL,
                        "id_type" INTEGER NOT NULL,
                        "price" REAL NOT NULL,
                        "count" INTEGER NOT NULL,
                        PRIMARY KEY("id_material" AUTOINCREMENT)
                        )'''
        )
        # таблица Авторы
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "Material" (
                        "id" INTEGER NOT NULL,
                        "name" TEXT NOT NULL,
                        PRIMARY KEY("id_author" AUTOINCREMENT)
                        )'''
        )
        # таблица Жанры
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "type" (
                        "ID" INTEGER NOT NULL,
                        "name_type" TEXT NOT NULL,
                        PRIMARY KEY("ID" AUTOINCREMENT)
                        )'''
        )

        self.conn.commit()


db = DB()
win = Main_Window()
win.root.mainloop()

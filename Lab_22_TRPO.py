import sqlite3
import tkinter as tk
from tkinter import ttk


# описываем класс Окно
class Main_Window():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("700x550")
        self.root.title("Книжный магазин")

        # логотип размещаем по центру окна
        self.logo = tk.PhotoImage(file="book.png")
        self.label = tk.Label(self.root, image=self.logo)
        self.label.pack(anchor='center', expand=1)

        # создаем меню
        self.main_menu = tk.Menu()

        self.file_menu = tk.Menu(tearoff=0)  # подменю
        self.ref_menu = tk.Menu(tearoff=0)  # подменю
        self.book_menu = tk.Menu(tearoff=0)  # подменю
        self.otch_menu = tk.Menu(tearoff=0)  # подменю
        self.help_menu = tk.Menu(tearoff=0)  # подменю

        self.file_menu.add_command(label="Выход", command=quit)

        self.ref_menu.add_command(label="Проставщики", command=self.open_win_provider)
        self.ref_menu.add_command(label="Издательства")
        self.ref_menu.add_command(label="Места издания")
        self.ref_menu.add_command(label="Авторы")
        self.ref_menu.add_command(label="Жанры")

        self.book_menu.add_command(label='Поступление книг')
        self.book_menu.add_command(label='Список книг')
        self.book_menu.add_command(label='Продажа книг')

        self.otch_menu.add_command(label="Отчет по поступлению")
        self.otch_menu.add_command(label="Отчет по остаткам")
        self.otch_menu.add_command(label="Отчет по продажам")

        self.help_menu.add_command(label="Руководство пользователя")
        self.help_menu.add_command(label="О программе")

        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
        self.main_menu.add_cascade(label="Справочники", menu=self.ref_menu)
        self.main_menu.add_cascade(label="Книги", menu=self.book_menu)
        self.main_menu.add_cascade(label="Отчеты", menu=self.otch_menu)
        self.main_menu.add_cascade(label="Справка", menu=self.help_menu)

        # привязываем меню к созданному окну
        self.root.config(menu=self.main_menu)

    def open_win_provider(self):
        self.root.withdraw()  # скрыть окно
        Provider_Window()


class Provider_Window():
    '''Окно Поставщики'''

    def __init__(self):
        self.root2 = tk.Tk()
        self.root2.geometry("800x500")
        self.root2.title("Книжный магазин/Поставщики")
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


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('book_bd.db')  # установили связь с БД (или создали если ее нет)
        self.c = self.conn.cursor()  # создали курсор
        # таблица Книги
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "book" (
                       "id_book" INTEGER NOT NULL,
                        "id_author" INTEGER,
                        "name" TEXT NOT NULL,
                        "id_genre" INTEGER NOT NULL,
                        "year_publishing" INTEGER NOT NULL,
                        "id_publishing_house" INTEGER NOT NULL,
                        "id_place_publication" INTEGER NOT NULL,
                        "number_pages" INTEGER NOT NULL,
                        "price" REAL NOT NULL,
                        "count" INTEGER NOT NULL,
                        PRIMARY KEY("id_book" AUTOINCREMENT)
                        )'''
        )
        # таблица Авторы
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "author" (
                        "id_author" INTEGER NOT NULL,
                        "name_author" TEXT NOT NULL,
                        PRIMARY KEY("id_author" AUTOINCREMENT)
                        )'''
        )
        # таблица Жанры
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "genre" (
                        "ID" INTEGER NOT NULL,
                        "name_genre" TEXT NOT NULL,
                        PRIMARY KEY("ID" AUTOINCREMENT)
                        )'''
        )
        # таблица Издательства
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "publish_house" (
                        "id_publish" INTEGER NOT NULL,
                        "name_publish" TEXT NOT NULL,
                        "address" TEXT NOT NULL,
                        "phone_number" TEXT NOT NULL,
                        PRIMARY KEY("id_publish" AUTOINCREMENT)
                        )'''
        )
        # таблица Места издания
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "place_publication" (
                        "id_place" INTEGER NOT NULL,
                        "name_place" TEXT NOT NULL,
                        PRIMARY KEY("id_place" AUTOINCREMENT)
                        )'''
        )

        self.conn.commit()


db = DB()
# создаем окно
win = Main_Window()
# запускаем окно
win.root.mainloop()

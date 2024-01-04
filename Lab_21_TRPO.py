import os,sys
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
import re
import pandas as pd

class Main_Window():

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

        self.material_menu.add_command(label='Передача в производство', command=self.open_win_receipt)
        self.material_menu.add_command(label='Список материалов', command=self.open_win_list)
        self.material_menu.add_command(label='Списание материалов')

        self.otch_menu.add_command(label="Отчет по поступлению")
        self.otch_menu.add_command(label="Отчет по передаче в производство")
        self.otch_menu.add_command(label="Отчет по списанию материалов")

        self.help_menu.add_command(label="Руководство пользователя" , command=self.open_management)
        self.help_menu.add_command(label="О программе" , command=self.open_win_prog)

        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
        self.main_menu.add_cascade(label="Справочники", menu=self.ref_menu)
        self.main_menu.add_cascade(label="Материалы", menu=self.material_menu)
        self.main_menu.add_cascade(label="Отчеты", menu=self.otch_menu)
        self.main_menu.add_cascade(label="Справка", menu=self.help_menu)

        # привязываем меню к созданному окну
        self.root.config(menu=self.main_menu)

    def open_management(self):
        os.system("guide.HTML")

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

    def open_win_prog(self):
        self.root.withdraw()
        prog_Window()


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
        self.table_pr = ttk.Treeview(self.table_frame,
                                     columns=('id_provider', 'name_provider', 'contact_person', 'phone_number'),
                                     height=15, show='headings')
        self.table_pr.column("id_provider", width=150, anchor=tk.NW)
        self.table_pr.column("name_provider", width=150, anchor=tk.NW)
        self.table_pr.column("contact_person", width=200, anchor=tk.NW)
        self.table_pr.column("phone_number", width=120, anchor=tk.CENTER)

        self.table_pr.heading("id_provider", text='id-поставщика')
        self.table_pr.heading("name_provider", text='Наименование')
        self.table_pr.heading("contact_person", text='Контактное лицо')
        self.table_pr.heading("phone_number", text='Номер телефона')

        self.view_info()

        # Полоса прокрутки
        self.scroll_bar = ttk.Scrollbar(self.table_frame)
        self.table_pr['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_pr.place(relx=0, rely=0, relheight=0.9, relwidth=0.97)

        # поле ввода и кнопка для поиска
        self.esearch = ttk.Entry(self.table_frame)
        self.esearch.place(relx=0.02, rely=0.92, relheight=0.05, relwidth=0.7)

        self.butsearch = tk.Button(self.table_frame, text="Найти", command=self.search_info)
        self.butsearch.place(relx=0.74, rely=0.92, relheight=0.05, relwidth=0.2)

        # поля для ввода
        self.lname = tk.Label(self.add_edit_frame, text="id постовщика")
        self.lname.place(relx=0.04, rely=0.02, relheight=0.05, relwidth=0.4)
        self.ename = ttk.Entry(self.add_edit_frame)
        self.ename.place(relx=0.45, rely=0.02, relheight=0.05, relwidth=0.5)

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
        self.butadd = tk.Button(self.add_edit_frame, text="Добавить запись", command=self.add_info)
        self.butadd.place(relx=0.1, rely=0.33, relheight=0.07, relwidth=0.8)

        self.butdel = tk.Button(self.add_edit_frame, text="Удалить запись", command=self.delete_info)
        self.butdel.place(relx=0.1, rely=0.44, relheight=0.07, relwidth=0.8)

        self.buted = tk.Button(self.add_edit_frame, text="Редактировать запись", command=self.update_info)
        self.buted.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

        self.butsave = tk.Button(self.add_edit_frame, text="Сохранить изменения", command=self.save_info)
        self.butsave.place(relx=0.1, rely=0.66, relheight=0.07, relwidth=0.8)

        self.butquit = tk.Button(self.add_edit_frame, text="Закрыть")
        self.butquit.place(relx=0.1, rely=0.88, relheight=0.07, relwidth=0.8)

    def quit_win_provider(self):
        self.root2.destroy()
        self.main_view.root.deiconify()

    def view_info(self):
        '''отобразить данные таблицы Поставщики'''
        self.db.c.execute('''SELECT name_provider, contact_person, phone_number FROM provider''')
        [self.table_pr.delete(i) for i in self.table_pr.get_children()]  # очистить таблицу для последующего обновления
        [self.table_pr.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_info(self):
        '''Удалить запись'''
        try:
            self.db.c.execute('''DELETE FROM provider WHERE name_provider=? AND contact_person=? AND phone_number=?''',
                              (self.table_pr.item(self.table_pr.selection())['values'][0],
                               self.table_pr.item(self.table_pr.selection())['values'][1],
                               '+' + str(self.table_pr.item(self.table_pr.selection())['values'][2])))
            self.db.conn.commit()
            self.view_info()
        except IndexError:
            showinfo(title="Внимание!", message="Выберите запись для удаления")

    def update_info(self):
        '''Редактировать запись'''
        try:
            self.ename.delete(0, tk.END)
            self.ename.insert(0, self.table_pr.item(self.table_pr.selection())['values'][0])
            self.econtact.delete(0, tk.END)
            self.econtact.insert(0, self.table_pr.item(self.table_pr.selection())['values'][1])
            self.ephone.delete(0, tk.END)
            self.ephone.insert(0, '+' + str(self.table_pr.item(self.table_pr.selection())['values'][2]))
        except IndexError:
            showerror(title="Внимание!", message="Выберите запись для редактирования")

    def save_info(self):
        '''Сохранить изменения'''
        self.db.c.execute('''SELECT * FROM provider''')
        provider_info = self.db.c.fetchall()
        for el in provider_info:
            if el[1] == self.table_pr.item(self.table_pr.selection())['values'][0] and el[2] == \
                    self.table_pr.item(self.table_pr.selection())['values'][1] and el[3] == '+' + str(
                self.table_pr.item(self.table_pr.selection())['values'][2]):
                id_provider = el[0]
                break

    def add_info(self):
        '''Добавить запись'''
        info_list_pr = [self.ename.get(), self.econtact.get(), self.ephone.get()]
        result = re.match("^\+{0,1}\d{0,12}$", info_list_pr[2])
        if '' in info_list_pr:  # валидация заполненя всех полей ввода
            showerror(title="Ошибка", message="Все поля должны быть заполнены")
        elif not result or len(info_list_pr[2]) != 13:  # валидация номера телефона для поля ввода
            showerror(title="Ошибка",
                      message="Номер телефона должен быть в формате +375xxxxxxxxx, где x представляет цифру")
        else:
            self.db.c.execute('''INSERT INTO provider(name_provider, contact_person, phone_number) VALUES (?, ?, ?)''',
                              (info_list_pr[0], info_list_pr[1], info_list_pr[2]))
            self.db.conn.commit()
            self.view_info()
            self.ename.delete(0, tk.END)
            self.econtact.delete(0, tk.END)
            self.ephone.delete(4, tk.END)

    def search_info(self):
        '''Кнопка Найти'''
        info = ('%' + self.esearch.get() + '%',)
        self.db.c.execute('''SELECT name_provider, contact_person, phone_number FROM provider 
                          WHERE name_provider LIKE ?''', info)
        [self.table_pr.delete(i) for i in self.table_pr.get_children()]  # очистить таблицу для последующего обновления
        [self.table_pr.insert('', 'end', values=row) for row in self.db.c.fetchall()]

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
        self.table_pr = ttk.Treeview(self.table_frame,
                                     columns=('id_type', 'name_type'),
                                     height=15, show='headings')
        self.table_pr.column("id_type", width=150, anchor=tk.NW)
        self.table_pr.column("name_type", width=150, anchor=tk.NW)

        self.table_pr.heading("id_type", text='id-типа')
        self.table_pr.heading("name_type", text='Наименование типа')

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
        self.ltype = tk.Label(self.add_edit_frame, text="Наименование")
        self.ltype.place(relx=0.04, rely=0.02, relheight=0.05, relwidth=0.4)
        self.etype = ttk.Entry(self.add_edit_frame)
        self.etype.place(relx=0.45, rely=0.02, relheight=0.05, relwidth=0.5)

        # кнопки
        self.butadd = tk.Button(self.add_edit_frame, text="Добавить запись", command=self.add_info)
        self.butadd.place(relx=0.1, rely=0.33, relheight=0.07, relwidth=0.8)

        self.butdel = tk.Button(self.add_edit_frame, text="Удалить запись", command=self.delete_info)
        self.butdel.place(relx=0.1, rely=0.44, relheight=0.07, relwidth=0.8)

        self.buted = tk.Button(self.add_edit_frame, text="Редактировать запись", command=self.update_info)
        self.buted.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

        self.butsave = tk.Button(self.add_edit_frame, text="Сохранить изменения", command=self.save_info)
        self.butsave.place(relx=0.1, rely=0.66, relheight=0.07, relwidth=0.8)

        self.butquit = tk.Button(self.add_edit_frame, text="Закрыть", command=self)
        self.butquit.place(relx=0.1, rely=0.77, relheight=0.07, relwidth=0.8)

    def quit_win_type(self):
        self.root3.destroy()
        self.main_view.root.deiconify()

    def view_info(self):
        '''отобразить данные таблицы Поставщики'''
        self.db.c.execute('''SELECT name_type FROM type''')
        [self.table_pr.delete(i) for i in self.table_pr.get_children()]  # очистить таблицу для последующего обновления
        [self.table_pr.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def add_info(self):
        '''Добавить запись'''
        self.db.c.execute('''INSERT INTO type(name_type) VALUES (?)''',
                          (self.etype.get(),))
        self.db.conn.commit()
        self.view_info()
        self.etype.delete(0, tk.END)

    def delete_info(self):
        '''Удалить запись'''
        try:
            self.db.c.execute('''DELETE FROM type WHERE name_type=?''',
                              (self.table_pr.item(self.table_pr.selection())['values']))
            self.db.conn.commit()
            self.view_info()
        except IndexError:
            showinfo(title="Внимание!", message="Выберите запись для удаления")

    def update_info(self):
        '''Редактировать запись'''
        try:
            self.etype.delete(0, tk.END)
            self.etype.insert(0, self.table_pr.item(self.table_pr.selection())['values'][0])
        except IndexError:
            showinfo(title="Внимание!", message="Выберите запись для редактирования")

    def save_info(self):
        '''Сохранить изменения'''
        self.db.c.execute('''SELECT * FROM type''')
        type_info = self.db.c.fetchall()
        for el in type_info:
            if el[1] == self.table_pr.item(self.table_pr.selection())['values']:
                id_type = el[0]
                break

    def search_info(self):
        '''Кнопка Найти'''
        info = ('%' + self.esearch.get() + '%',)
        self.db.c.execute('''SELECT name_type FROM type 
                          WHERE name_type LIKE ?''', info)
        [self.table_pr.delete(i) for i in self.table_pr.get_children()]  # очистить таблицу для последующего обновления
        [self.table_pr.insert('', 'end', values=row) for row in self.db.c.fetchall()]

class receipts_Window():

    def __init__(self):
        self.root2 = tk.Tk()
        self.root2.geometry("1300x400")
        self.root2.title("Материальный склад/Материалы")
        self.root2.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())  # перехват кнопки Х
        self.main_view = win
        self.db = db

        self.label = tk.Label(self.root2, text="Материалы")
        self.label.pack(anchor='nw')

        self.button_toexcel = tk.Button(self.root2, text="Экспорт в Excel", command=self.toexcel_book)
        self.button_toexcel.pack(anchor='nw', expand=1)

        self.tree = ttk.Treeview(self.root2, columns=('id_materia', 'name', 'price', 'count'),
                                 height=15, show='headings')
        self.tree.column("id_materia", width=230, anchor=tk.NW)
        self.tree.column("name", width=300, anchor=tk.NW)
        self.tree.column("price", width=225, anchor=tk.CENTER)
        self.tree.column("count", width=50, anchor=tk.CENTER)

        self.tree.heading("id_materia", text='id материала')
        self.tree.heading("name", text='Название')
        self.tree.heading("price", text='Цена (руб.)')
        self.tree.heading("count", text='К-во экз')
        self.tree.heading("price", text='Цена (руб.)')
        self.tree.heading("count", text='К-во экз')

        # Полоса прокрутки
        self.scroll_bar = ttk.Scrollbar(self.root2, command=self.tree.yview)
        self.tree['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.pack()

        self.button_quit = tk.Button(self.root2, text="Закрыть", command=lambda: self.quit_win())
        self.button_quit.pack(anchor='sw', expand=1)

        self.view_records_book()

    def record(self, id_materia, name, id_type, id_provider, name_provider, price, count):
        '''обновление и вызов функции для отображения данных'''
        self.db.save_data_book(id_materia, name, id_type, id_provider, name_provider, price, count)
        self.view_records_book()

    def view_records_book(self):
        '''отобразить данные таблицы Книги'''
        self.db.c.execute('''SELECT id_material, name, id_type, price, count FROM material''')
        [self.tree.delete(i) for i in self.tree.get_children()]  # очистить таблицу для последующего обновления
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def update_records_book(self, id_materia, name, id_type, id_provider, name_provider, price, count):
        self.db.c.execute('''UPDATE book SET id_materia=?, name=?, id_type=?, id_provider=?, name_provider=?,
                          price=?, count=? WHERE ID=?''',
                          (id_materia, name, id_type, id_provider, name_provider, price, count,
                           self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records_book()

    def quit_win(self):
        self.root2.destroy()
        self.main_view.root.deiconify()

    def toexcel_book(self):
        self.db.c.execute('''SELECT * FROM material''')
        materia_list = self.db.c.fetchall()
        # Используем словарь для заполнения DataFrame
        # Ключи в словаре — это названия колонок. А значения - строки с информацией
        df = pd.DataFrame({'ID материала': [el[1] for el in materia_list],
                           'Название': [el[2] for el in materia_list],
                           'Цена (руб.)': [el[3] for el in materia_list]})
        # указажем writer библиотеки
        writer = pd.ExcelWriter('example.xlsx', engine="xlsxwriter")
        # записшем наш DataFrame в файл
        df.to_excel(writer, 'Sheet1')
        # сохраним результат
        writer.close()

class list_Window():
    def __init__(self):
        self.root2 = tk.Tk()
        self.root2.geometry("1300x400")
        self.root2.title("Материальный склад/Материалы")
        self.root2.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())  # перехват кнопки Х
        self.main_view = win
        self.db = db

        self.label = tk.Label(self.root2, text="Материалы")
        self.label.pack(anchor='nw')

        self.button_toexcel = tk.Button(self.root2, text="Экспорт в Excel", command=self.toexcel_book)
        self.button_toexcel.pack(anchor='nw', expand=1)

        self.tree = ttk.Treeview(self.root2, columns=('id_materia', 'name', 'price', 'count'),
                                 height=15, show='headings')
        self.tree.column("id_materia", width=230, anchor=tk.NW)
        self.tree.column("name", width=300, anchor=tk.NW)
        self.tree.column("price", width=225, anchor=tk.CENTER)
        self.tree.column("count", width=50, anchor=tk.CENTER)

        self.tree.heading("id_materia", text='id материала')
        self.tree.heading("name", text='Название')
        self.tree.heading("price", text='Цена (руб.)')
        self.tree.heading("count", text='К-во экз')
        self.tree.heading("price", text='Цена (руб.)')
        self.tree.heading("count", text='К-во экз')

        # Полоса прокрутки
        self.scroll_bar = ttk.Scrollbar(self.root2, command=self.tree.yview)
        self.tree['yscrollcommand'] = self.scroll_bar.set
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.pack()

        self.button_quit = tk.Button(self.root2, text="Закрыть", command=lambda: self.quit_win())
        self.button_quit.pack(anchor='sw', expand=1)

        self.view_records_book()

    def record(self, id_materia, name, id_type, id_provider, name_provider, price, count):
        '''обновление и вызов функции для отображения данных'''
        self.db.save_data_book(id_materia, name, id_type, id_provider, name_provider, price, count)
        self.view_records_book()

    def view_records_book(self):
        '''отобразить данные таблицы Книги'''
        self.db.c.execute('''SELECT id_material, name, id_type, price, count FROM material''')
        [self.tree.delete(i) for i in self.tree.get_children()]  # очистить таблицу для последующего обновления
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def update_records_book(self, id_materia, name, id_type, id_provider, name_provider, price, count):
        self.db.c.execute('''UPDATE book SET id_materia=?, name=?, id_type=?, id_provider=?, name_provider=?,
                          price=?, count=? WHERE ID=?''',
                          (id_materia, name, id_type, id_provider, name_provider, price, count,
                           self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records_book()

    def quit_win(self):
        self.root2.destroy()
        self.main_view.root.deiconify()

    def toexcel_book(self):
        self.db.c.execute('''SELECT * FROM material''')
        materia_list = self.db.c.fetchall()
        # Используем словарь для заполнения DataFrame
        # Ключи в словаре — это названия колонок. А значения - строки с информацией
        df = pd.DataFrame({'ID материала': [el[1] for el in materia_list],
                           'Название': [el[2] for el in materia_list],
                           'Цена (руб.)': [el[3] for el in materia_list]})
        # указажем writer библиотеки
        writer = pd.ExcelWriter('example.xlsx', engine="xlsxwriter")
        # записшем наш DataFrame в файл
        df.to_excel(writer, 'Sheet1')
        # сохраним результат
        writer.close()

class prog_Window():
    def __init__(self):
        self.root2 = tk.Tk()
        self.root2.geometry("400x100")
        self.root2.title("Материальный склад/о Программе")
        self.root2.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())  # перехват кнопки Х
        self.main_view = win
        self.db = db

        self.label = tk.Label(self.root2, text="Иванов Евгений Максимович\nПО-31\nВерсия 0.2")
        self.label.pack(anchor='center')

    def quit_win(self):
        self.root2.destroy()
        self.main_view.root.deiconify()

class AP():
    def __init__(self):
        self.conn = os.system('О программе.HTML')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('material_bd.db')  # установили связь с БД (или создали если ее нет)
        self.c = self.conn.cursor()  # создали курсор
        # таблица Книги

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "provider" (
                       "id_provider" INTEGER NOT NULL,
                       "name_provider" TEXT NOT NULL,
                       "contact_person" TEXT NOT NULL,
                       "phone_number" TEXT NOT NULL,
                        PRIMARY KEY("id_provider" AUTOINCREMENT)
                        )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "material" (
                       "id_material" INTEGER NOT NULL,
                        "name" TEXT NOT NULL,
                        "price" REAL NOT NULL,
                        "count" INTEGER NOT NULL,
                        PRIMARY KEY("id_material" AUTOINCREMENT)
                        )'''
        )
        # таблица Жанры
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "type" (
                        "id_type" INTEGER NOT NULL,
                        "name_type" TEXT NOT NULL,
                        PRIMARY KEY("id_type" AUTOINCREMENT)
                        )'''
        )

        self.conn.commit()

db = DB()
win = Main_Window()
win.root.mainloop()
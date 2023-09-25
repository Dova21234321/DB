import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('Lab_18_TRPO.db')  # установили связь с БД (или создали если ее нет)
        self.c = self.conn.cursor()  # создали курсор
        # таблица  материалы
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "material" (
                       "id_material" INTEGER NOT NULL,
                        "id_supplier" INTEGER,
                        "name" TEXT NOT NULL,
                        "id_type" INTEGER NOT NULL,
                        "price" REAL NOT NULL,
                        "count" INTEGER NOT NULL,
                        PRIMARY KEY("id_material" AUTOINCREMENT)
                        )'''
        )
        # таблица поставщики
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "supplier" (
                        "id_supplier" INTEGER NOT NULL,
                        "name_supplier" TEXT NOT NULL,
                        PRIMARY KEY("id_supplier" AUTOINCREMENT)
                        )'''
        )
        # таблица типы
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "type" (
                        "id_type" INTEGER NOT NULL,
                        "name_type" TEXT NOT NULL,
                        PRIMARY KEY("id_type" AUTOINCREMENT)
                        )'''
        )
        self.conn.commit()

db = DB()

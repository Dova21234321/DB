import sqlite3

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

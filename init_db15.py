#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных фильмов
"""

import sqlite3
import os

def init_database():
    """Инициализация базы данных"""
    
    # Удаляем старую базу данных если существует
    if os.path.exists('films.db'):
        os.remove('films.db')
        print("Старая база данных удалена")
    
    # Создаём новую базу данных
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()
    
    # Создаём таблицу фильмов
    cursor.execute('''
        CREATE TABLE films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            title_ru TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            CHECK (year >= 1895),
            CHECK (LENGTH(description) <= 2000),
            CHECK (LENGTH(title) <= 200),
            CHECK (LENGTH(title_ru) <= 200)
        )
    ''')
    
    # Добавляем индекс для быстрого поиска по году
    cursor.execute('CREATE INDEX idx_films_year ON films(year)')
    
    # Добавляем начальные данные
    initial_films = [
        ("Interstellar", "Интерстеллар", 2014, 
         "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."),
        ("The Shawshank Redemption", "Побег из Шоушенка", 1994,
         "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящим по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."),
        ("The Green Mile", "Зеленая миля", 1999,
         "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора». Каждый из узников которого однажды проходит зелёную милю..."),
        ("Fight Club", "Бойцовский клуб", 1999,
         "Страховой сотрудник разрушает свою рутинную благополучную жизнь и создаёт подпольный бойцовский клуб, который превращается в нечто большее."),
        ("Léon", "Леон", 1994,
         "Профессиональный убийца Леон неожиданно для себя самого решает помочь 12-летней соседке Матильде, чья семья была убита коррумпированными полицейскими.")
    ]
    
    cursor.executemany('''
        INSERT INTO films (title, title_ru, year, description) 
        VALUES (?, ?, ?, ?)
    ''', initial_films)
    
    conn.commit()
    
    # Проверяем создание
    cursor.execute('SELECT COUNT(*) FROM films')
    count = cursor.fetchone()[0]
    
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    
    conn.close()
    
    print(f"База данных успешно создана!")
    print(f"Созданы таблицы: {[t[0] for t in tables]}")
    print(f"Добавлено фильмов: {count}")
    print(f"Файл базы данных: films.db")
    print(f"Размер файла: {os.path.getsize('films.db')} байт")

if __name__ == '__main__':
    init_database()
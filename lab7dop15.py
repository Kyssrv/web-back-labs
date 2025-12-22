from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import sqlite3
import os

lab7 = Blueprint('lab7', __name__)

# Функция для получения соединения с БД
def get_db_connection():
    conn = sqlite3.connect('films.db')
    conn.row_factory = sqlite3.Row
    return conn

# Инициализация БД
def init_db():
    if not os.path.exists('films.db'):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Создание таблицы фильмов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                year INTEGER NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Добавление начальных данных
        initial_films = [
            ("Interstellar", "Интерстеллар", 2014, 
             "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."),
            ("The Shawshank Redemption", "Побег из Шоушенка", 1994,
             "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящим по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."),
            ("The Green Mile", "Зеленая миля", 1999,
             "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора». Каждый из узников которого однажды проходит зелёную милю...")
        ]
        
        cursor.executemany('''
            INSERT INTO films (title, title_ru, year, description) 
            VALUES (?, ?, ?, ?)
        ''', initial_films)
        
        conn.commit()
        conn.close()

# Инициализируем БД при импорте
init_db()

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

# Валидация данных фильма
def validate_film(film, is_update=False):
    errors = {}
    
    # Валидация русского названия
    title_ru = film.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Русское название обязательно'
    elif len(title_ru) > 200:
        errors['title_ru'] = 'Русское название не должно превышать 200 символов'
    
    # Валидация оригинального названия
    title = film.get('title', '').strip()
    if not title and not title_ru:
        errors['title'] = 'Хотя бы одно название должно быть заполнено'
    elif len(title) > 200:
        errors['title'] = 'Оригинальное название не должно превышать 200 символов'
    
    # Валидация года
    year_str = film.get('year', '')
    if not year_str:
        errors['year'] = 'Год обязателен'
    else:
        try:
            year = int(year_str)
            current_year = datetime.now().year
            if year < 1895:
                errors['year'] = f'Год не может быть раньше 1895 (первый фильм)'
            elif year > current_year:
                errors['year'] = f'Год не может быть больше {current_year}'
        except ValueError:
            errors['year'] = 'Год должен быть числом'
    
    # Валидация описания
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно'
    elif len(description) > 2000:
        errors['description'] = f'Описание не должно превышать 2000 символов (сейчас: {len(description)})'
    elif len(description) < 10:
        errors['description'] = 'Описание должно содержать минимум 10 символов'
    
    return errors

# Получение всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM films ORDER BY year DESC')
    films = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(films)

# Получение одного фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM films WHERE id = ?', (id,))
    film = cursor.fetchone()
    
    conn.close()
    
    if film is None:
        return {'error': 'Фильм не найден'}, 404
    
    return jsonify(dict(film))

# Удаление фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Проверяем существование фильма
    cursor.execute('SELECT id FROM films WHERE id = ?', (id,))
    if cursor.fetchone() is None:
        conn.close()
        return {'error': 'Фильм не найден'}, 404
    
    cursor.execute('DELETE FROM films WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return '', 204

# Редактирование фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Проверяем существование фильма
    cursor.execute('SELECT id FROM films WHERE id = ?', (id,))
    if cursor.fetchone() is None:
        conn.close()
        return {'error': 'Фильм не найден'}, 404
    
    film = request.get_json()
    
    # Если оригинальное название пустое, а русское задано - копируем русское
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']
    
    # Валидация
    errors = validate_film(film, is_update=True)
    if errors:
        conn.close()
        return jsonify(errors), 400
    
    # Обновление в БД
    cursor.execute('''
        UPDATE films 
        SET title = ?, title_ru = ?, year = ?, description = ? 
        WHERE id = ?
    ''', (
        film['title'],
        film['title_ru'],
        int(film['year']),
        film['description'],
        id
    ))
    
    conn.commit()
    
    # Получаем обновлённый фильм
    cursor.execute('SELECT * FROM films WHERE id = ?', (id,))
    updated_film = dict(cursor.fetchone())
    
    conn.close()
    return jsonify(updated_film)

# Добавление нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    # Если оригинальное название пустое, а русское задано - копируем русское
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']
    
    # Валидация
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Вставка в БД
    cursor.execute('''
        INSERT INTO films (title, title_ru, year, description) 
        VALUES (?, ?, ?, ?)
    ''', (
        film['title'],
        film['title_ru'],
        int(film['year']),
        film['description']
    ))
    
    new_id = cursor.lastrowid
    conn.commit()
    
    # Получаем созданный фильм
    cursor.execute('SELECT * FROM films WHERE id = ?', (new_id,))
    created_film = dict(cursor.fetchone())
    
    conn.close()
    return jsonify(created_film), 201

# Статистика фильмов
@lab7.route('/lab7/rest-api/stats/', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Получаем статистику
    cursor.execute('SELECT COUNT(*) as total FROM films')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT MIN(year) as min_year, MAX(year) as max_year FROM films')
    years = cursor.fetchone()
    
    cursor.execute('SELECT AVG(year) as avg_year FROM films')
    avg_year = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_films': total,
        'min_year': years[0],
        'max_year': years[1],
        'avg_year': round(avg_year, 1) if avg_year else 0
    })
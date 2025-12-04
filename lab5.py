# lab5.py
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

def get_db_connection():
    """Функция для подключения к базе данных"""
    conn = psycopg2.connect(
        host='localhost',
        database='kucherova_sofia_knowledge_base',
        user='kucherova_sofia_knowledge_base',
        password='123'
    )
    return conn

@lab5.route('/lab5')
def main():
    username = session.get('login', 'anonymous')
    return render_template('lab5/lab5.html', username=username)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    # Получаем данные из формы
    login = request.form.get('login')
    password = request.form.get('password')
    
    # Проверяем, что оба поля заполнены
    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')
    
    # Подключаемся к базе данных
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Проверяем, существует ли пользователь с таким логином
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        existing_user = cur.fetchone()
        
        if existing_user:
            cur.close()
            conn.close()
            return render_template('lab5/register.html', error='Такой пользователь уже существует')
        
        # Добавляем нового пользователя
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))
        
        # Сохраняем изменения в БД
        conn.commit()
        
        cur.close()
        conn.close()
        
        # Перенаправляем на страницу успеха
        return render_template('lab5/success.html', login=login)
        
    except Exception as e:
        # В случае ошибки закрываем соединение и показываем сообщение
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error=f'Ошибка при регистрации: {str(e)}')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    # Временная заглушка для POST запроса
    return redirect(url_for('lab5.main'))

@lab5.route('/lab5/list')
def list_articles():
    return "Список статей - будет реализован позже"

@lab5.route('/lab5/create')
def create():
    return "Создание статьи - будет реализовано позже"

@lab5.route('/lab5/test_db')
def test_db():
    """Тестовая страница для проверки подключения к БД"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Проверяем таблицы
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cur.fetchall()
        
        # Проверяем пользователей
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        
        cur.close()
        conn.close()
        
        tables_list = [table['table_name'] for table in tables]
        users_count = len(users)
        
        return f"""
        <h2>Проверка базы данных</h2>
        <p><strong>Таблицы в БД:</strong> {tables_list}</p>
        <p><strong>Количество пользователей:</strong> {users_count}</p>
        <p><a href="/lab5">Вернуться на главную</a></p>
        """
    
    except Exception as e:
        return f"Ошибка подключения к БД: {str(e)}"
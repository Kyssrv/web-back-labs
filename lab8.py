from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import db
from db.models import users, articles
from werkzeug.security import generate_password_hash, check_password_hash

lab8 = Blueprint('lab8', __name__)

# Главная страница лабораторной работы 8
@lab8.route('/lab8/')
def index():
    # Получаем имя пользователя из сессии или используем 'anonymous'
    username = session.get('username', 'anonymous')
    return render_template('lab8/index.html', username=username)

# РЕГИСТРАЦИЯ
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Показываем форму регистрации
        return render_template('lab8/register.html')
    
    # Получаем данные из формы
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()
    
    # Проверка на пустые поля
    if not login_form:
        return render_template('lab8/register.html', 
                             error='Имя пользователя не может быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html', 
                             error='Пароль не может быть пустым')
    
    # Проверка минимальной длины пароля (опционально, но рекомендуется)
    if len(password_form) < 3:
        return render_template('lab8/register.html', 
                             error='Пароль должен содержать минимум 3 символа')
    
    # Проверка существования пользователя с таким логином
    login_exists = users.query.filter_by(login=login_form).first()
    
    if login_exists:
        return render_template('lab8/register.html', 
                             error='Такой пользователь уже существует')
    
    try:
        # Хешируем пароль
        password_hash = generate_password_hash(password_form)
        
        # Создаем нового пользователя
        new_user = users(login=login_form, password=password_hash)
        
        # Добавляем в сессию и сохраняем в БД
        db.session.add(new_user)
        db.session.commit()
        
        # Автоматически авторизуем пользователя после регистрации
        session['username'] = login_form
        session['user_id'] = new_user.id
        
        # Перенаправляем на главную страницу
        return redirect('/lab8/')
    
    except Exception as e:
        # Откатываем изменения в случае ошибки
        db.session.rollback()
        return render_template('lab8/register.html', 
                             error=f'Ошибка при регистрации: {str(e)}')

# АВТОРИЗАЦИЯ (заглушка, будет реализована позже)
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    # POST-запрос будет обработан позже
    return "Авторизация (будет реализована позже)"

# ВЫХОД
@lab8.route('/lab8/logout')
def logout():
    # Очищаем сессию
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/lab8/')

# СПИСОК СТАТЕЙ
@lab8.route('/lab8/articles')
def articles_list():
    # Проверяем авторизацию
    user_id = session.get('user_id')
    
    if user_id:
        # Получаем статьи текущего пользователя
        user_articles = articles.query.filter_by(login_id=user_id).all()
        return render_template('lab8/articles.html', 
                             articles=user_articles, 
                             username=session.get('username'))
    else:
        # Показываем сообщение о необходимости авторизации
        return redirect('/lab8/login')

# СОЗДАНИЕ СТАТЬИ
@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create_article():
    # Проверяем авторизацию
    if 'user_id' not in session:
        return redirect('/lab8/login')
    
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    # POST-запрос будет обработан позже
    return "Создание статьи (будет реализовано позже)"

# ТЕСТОВЫЙ МАРШРУТ для проверки регистрации
@lab8.route('/lab8/test-users')
def test_users():
    try:
        # Получаем всех пользователей из БД
        all_users = users.query.all()
        
        result = "<h1>Тест регистрации - Список пользователей</h1>"
        result += f"<p>Всего пользователей: {len(all_users)}</p>"
        
        if all_users:
            result += "<ul>"
            for user in all_users:
                result += f"<li>ID: {user.id}, Логин: {user.login}, Пароль (хеш): {user.password[:30]}...</li>"
            result += "</ul>"
        else:
            result += "<p>Пользователей пока нет.</p>"
        
        result += '<p><a href="/lab8/">Вернуться на главную</a></p>'
        
        return result
    except Exception as e:
        return f"<h1>Ошибка</h1><p>{str(e)}</p>"
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from db.models import users, articles
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

lab8 = Blueprint('lab8', __name__)

# Главная страница лабораторной работы 8
@lab8.route('/lab8/')
def index():
    # Используем current_user из Flask-Login
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/index.html', username=username)

# РЕГИСТРАЦИЯ (обновленная с Flask-Login)
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Если пользователь уже авторизован, перенаправляем на главную
        if current_user.is_authenticated:
            return redirect('/lab8/')
        return render_template('lab8/register.html')
    
    # Получаем данные из формы
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    
    # Проверка на пустые поля
    errors = []
    if not login_form:
        errors.append('Имя пользователя не может быть пустым')
    
    if not password_form:
        errors.append('Пароль не может быть пустым')
    
    if password_form != confirm_password:
        errors.append('Пароли не совпадают')
    
    # Проверка минимальной длины
    if len(password_form) < 3:
        errors.append('Пароль должен содержать минимум 3 символа')
    
    if errors:
        return render_template('lab8/register.html', error='; '.join(errors))
    
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
        
        # Автоматически авторизуем пользователя после регистрации с Flask-Login
        login_user(new_user, remember=False)
        
        # Перенаправляем на главную страницу
        return redirect('/lab8/')
    
    except Exception as e:
        # Откатываем изменения в случае ошибки
        db.session.rollback()
        return render_template('lab8/register.html', 
                             error=f'Ошибка при регистрации: {str(e)}')

# АВТОРИЗАЦИЯ (полная реализация с Flask-Login)
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже авторизован, перенаправляем на главную
    if current_user.is_authenticated:
        return redirect('/lab8/')
    
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    # Получаем данные из формы
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()
    remember = True if request.form.get('remember') else False
    
    # Проверка на пустые поля
    if not login_form or not password_form:
        return render_template('lab8/login.html', 
                             error='Логин и пароль не могут быть пустыми')
    
    # Ищем пользователя в БД
    user = users.query.filter_by(login=login_form).first()
    
    # Проверяем пользователя и пароль
    if user and check_password_hash(user.password, password_form):
        # Авторизуем пользователя через Flask-Login
        login_user(user, remember=remember)
        
        # Перенаправляем на следующую страницу или главную
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect('/lab8/')
    
    # Если авторизация не удалась
    return render_template('lab8/login.html', 
                         error='Ошибка входа: неверный логин или пароль')

# ВЫХОД с Flask-Login
@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

# СПИСОК СТАТЕЙ (только для авторизованных пользователей)
@lab8.route('/lab8/articles/')
@login_required
def article_list():
    # Получаем статьи текущего пользователя
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    
    # Получаем публичные статьи других пользователей
    public_articles = articles.query.filter_by(is_public=True).all()
    
    return render_template('lab8/articles.html', 
                         user_articles=user_articles,
                         public_articles=[article for article in public_articles 
                                         if article.login_id != current_user.id])

# СОЗДАНИЕ СТАТЬИ (только для авторизованных пользователей)
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    # Получаем данные из формы
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_public = True if request.form.get('is_public') else False
    is_favorite = True if request.form.get('is_favorite') else False
    
    # Проверка на пустые поля
    if not title or not article_text:
        return render_template('lab8/create.html', 
                             error='Заголовок и текст не могут быть пустыми')
    
    try:
        # Создаем новую статью
        new_article = articles(
            login_id=current_user.id,
            title=title,
            article_text=article_text,
            is_public=is_public,
            is_favorite=is_favorite
        )
        
        # Добавляем и сохраняем
        db.session.add(new_article)
        db.session.commit()
        
        # Перенаправляем на список статей
        return redirect('/lab8/articles/')
    
    except Exception as e:
        db.session.rollback()
        return render_template('lab8/create.html', 
                             error=f'Ошибка при создании статьи: {str(e)}')

# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ (только для авторизованных)
@lab8.route('/lab8/profile')
@login_required
def profile():
    # Статистика пользователя
    articles_count = articles.query.filter_by(login_id=current_user.id).count()
    public_articles_count = articles.query.filter_by(
        login_id=current_user.id, 
        is_public=True
    ).count()
    favorite_articles_count = articles.query.filter_by(
        login_id=current_user.id, 
        is_favorite=True
    ).count()
    
    return render_template('lab8/profile.html',
                         user=current_user,
                         articles_count=articles_count,
                         public_articles_count=public_articles_count,
                         favorite_articles_count=favorite_articles_count)

# ТЕСТОВЫЙ МАРШРУТ для проверки авторизации
@lab8.route('/lab8/secure-test')
@login_required
def secure_test():
    return f'''
    <h1>Защищенная страница</h1>
    <p>Вы успешно авторизованы как <strong>{current_user.login}</strong></p>
    <p>ID пользователя: {current_user.id}</p>
    <p><a href="/lab8/">На главную</a></p>
    '''

# ТЕСТОВЫЙ МАРШРУТ для проверки пользователей
@lab8.route('/lab8/test-users')
def test_users():
    try:
        # Получаем всех пользователей из БД
        all_users = users.query.all()
        
        result = "<h1>Тест авторизации - Список пользователей</h1>"
        result += f"<p>Всего пользователей: {len(all_users)}</p>"
        result += f"<p>Текущий пользователь: {current_user.login if current_user.is_authenticated else 'Не авторизован'}</p>"
        
        if all_users:
            result += "<table border='1' style='border-collapse: collapse;'>"
            result += "<tr><th>ID</th><th>Логин</th><th>Пароль (хеш)</th><th>Статей</th></tr>"
            for user in all_users:
                articles_count = articles.query.filter_by(login_id=user.id).count()
                result += f"<tr><td>{user.id}</td><td>{user.login}</td><td>{user.password[:30]}...</td><td>{articles_count}</td></tr>"
            result += "</table>"
        else:
            result += "<p>Пользователей пока нет.</p>"
        
        result += '<p><a href="/lab8/">Вернуться на главную</a></p>'
        
        return result
    except Exception as e:
        return f"<h1>Ошибка</h1><p>{str(e)}</p>"
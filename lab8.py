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

# РЕГИСТРАЦИЯ
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Если пользователь уже авторизован, перенаправляем на главную
        if current_user.is_authenticated:
            return redirect('/lab8/')
        return render_template('lab8/register.html')
    
    # ... остальной код регистрации ...
    return render_template('lab8/register.html', 
                         error='Ошибка при регистрации')

# АВТОРИЗАЦИЯ
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже авторизован, перенаправляем на главную
    if current_user.is_authenticated:
        return redirect('/lab8/')
    
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    # ... остальной код авторизации ...
    return render_template('lab8/login.html', 
                         error='Ошибка входа: неверный логин или пароль')

# ВЫХОД ИЗ СИСТЕМЫ (ЛОГАУТ)
@lab8.route('/lab8/logout')
@login_required  # Только авторизованные пользователи могут выходить
def logout():
    # Выходим из системы
    logout_user()
    
    # Показываем сообщение об успешном выходе
    flash('Вы успешно вышли из системы', 'success')
    
    # Перенаправляем на главную страницу
    return redirect('/lab8/')

# УЛУЧШЕННАЯ ВЕРСИЯ С ПОДТВЕРЖДЕНИЕМ
@lab8.route('/lab8/logout-confirm')
@login_required
def logout_confirm():
    """Страница подтверждения выхода"""
    return render_template('lab8/logout_confirm.html')

@lab8.route('/lab8/logout-action', methods=['POST'])
@login_required
def logout_action():
    """Действие выхода (после подтверждения)"""
    # Получаем данные из формы
    confirm = request.form.get('confirm')
    
    if confirm == 'yes':
        # Запоминаем имя пользователя для сообщения
        username = current_user.login
        
        # Выходим из системы
        logout_user()
        
        # Показываем сообщение об успешном выходе
        flash(f'Пользователь {username} успешно вышел из системы', 'success')
        
        # Перенаправляем на главную страницу
        return redirect('/lab8/')
    else:
        # Если пользователь передумал, возвращаем на главную
        flash('Выход отменен', 'info')
        return redirect('/lab8/')

# АЛЬТЕРНАТИВНЫЙ ВАРИАНТ С AJAX (для современных интерфейсов)
@lab8.route('/lab8/api/logout', methods=['POST'])
@login_required
def api_logout():
    """API для выхода из системы (для AJAX запросов)"""
    try:
        # Запоминаем данные пользователя
        user_data = {
            'id': current_user.id,
            'login': current_user.login
        }
        
        # Выходим из системы
        logout_user()
        
        # Возвращаем JSON ответ
        return {
            'success': True,
            'message': 'Вы успешно вышли из системы',
            'user': user_data,
            'redirect': '/lab8/'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }, 500

# СПИСОК СТАТЕЙ (только для авторизованных пользователей)
@lab8.route('/lab8/articles/')
@login_required
def article_list():
    # ... код для получения статей ...
    return render_template('lab8/articles.html',
                         user_articles=[],
                         public_articles=[])

# СОЗДАНИЕ СТАТЬИ (только для авторизованных пользователей)
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    # ... код создания статьи ...
    return redirect('/lab8/articles/')

# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ (только для авторизованных)
@lab8.route('/lab8/profile')
@login_required
def profile():
    # Статистика пользователя
    articles_count = 0  # Заглушка
    public_articles_count = 0  # Заглушка
    favorite_articles_count = 0  # Заглушка
    
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
    <p><a href="/lab8/">На главную</a> | <a href="/lab8/logout">Выйти</a></p>
    '''

# СТРАНИЦА НАСТРОЕК С ВОЗМОЖНОСТЬЮ ВЫХОДА
@lab8.route('/lab8/settings')
@login_required
def settings():
    """Страница настроек пользователя"""
    return render_template('lab8/settings.html', user=current_user)

# КОНТРОЛЬНАЯ ПАНЕЛЬ (только для авторизованных)
@lab8.route('/lab8/dashboard')
@login_required
def dashboard():
    """Панель управления пользователя"""
    return render_template('lab8/dashboard.html', user=current_user)
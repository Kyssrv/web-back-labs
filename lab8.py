from flask import Blueprint, render_template

# Создаем Blueprint для лабораторной работы 8
lab8 = Blueprint('lab8', __name__)

# Главная страница лабораторной работы 8
@lab8.route('/lab8/')
def index():
    # Пока используем 'anonymous', позже заменим на реальное имя пользователя
    return render_template('lab8/index.html', username='anonymous')

# Заглушки для остальных маршрутов (реализуем позже)
@lab8.route('/lab8/login')
def login():
    return "Страница входа (будет реализована позже)"

@lab8.route('/lab8/register')
def register():
    return "Страница регистрации (будет реализована позже)"

@lab8.route('/lab8/articles')
def articles():
    return "Список статей (будет реализован позже)"

@lab8.route('/lab8/create')
def create():
    return "Создание статьи (будет реализовано позже)"
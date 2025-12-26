from flask import Flask
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

app = Flask(__name__)

# Секретный ключ для сессий
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')

# Определяем тип БД (postgres или sqlite)
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

# Настройка подключения к БД в зависимости от типа
if app.config['DB_TYPE'] == 'postgres':
    # Настройки для PostgreSQL (локальная разработка)
    db_name = 'ivan_ivanov_orm'
    db_user = 'ivan_ivanov_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    # Настройки для SQLite (удаленный хостинг)
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "ivan_ivanov_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Отключаем уведомления о модификациях
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем БД с приложением
db.init_app(app)

# НАСТРОЙКА FLASK-LOGIN
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'  # Куда перенаправлять неавторизованных пользователей
login_manager.init_app(app)

# Функция для загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# Регистрируем Blueprint'ы лабораторных работ
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)


# Глобальные переменные
count = 0
flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
access_log = []

@app.route("/")
@app.route("/index")
def index():
    return """<!doctype html>
<html>
    <head>
        <title>HTTP, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>HTTP, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <main>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                    <li><a href="/lab3">Третья лабораторная</a></li>
                    <li><a href="/lab4">Четвертая лабораторная</a></li>
                    <li><a href="/lab5">Пятая лабораторная</a></li>
                    <li><a href="/lab6">6 лабораторная</a></li>
                    <li><a href="/lab7">7 лабораторная</a></li>
                    <li><a href="/lab8">8 лабораторная</a></li>
                </ul>
            </nav>
        </main>
        <footer>
            Кучерова София Владимировна, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>"""

@app.route('/start')
def start():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>НГТУ, ФБ, Лабораторные работы</title>
</head>
<body>
    <header>
        НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
    </header>
    
    <div>
        <a href="/lab1">Первая лабораторная</a>
    </div>
    
    <div>
        <a href="/lab2">Вторая лабораторная</a>
    </div>
    
    <div>
        <a href="/lab3">Третья лабораторная</a>
    </div>
    
    <div>
        <a href="/lab4">Четвертая лабораторная</a>
    </div>

    <div>
        <a href="/lab5">Пятая лабораторная</a>
    </div>
    
    <div>
        <a href="/lab6">Шестая лабораторная</a>
    </div>

    <div>
        <a href="/lab7">Седьмая лабораторная</a>
    </div>

    <div>
        <a href="/lab8">Восьмая лабораторная</a>
    </div>

    <footer>
        &copy; София Кучерова, ФБИ-33, 2025
    </footer>
</body>
</html>'''

# Обработчики ошибок
@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    current_time = datetime.datetime.now()
    accessed_url = request.url
    
    # Логируем доступ
    access_log.append(f"{current_time}, пользователь {client_ip} зашёл на адрес: {accessed_url}")
    
    return f"""<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
    </head>
    <body>
        <h1>404 - Страница не найдена</h1>
        <p>Запрошенная страница не существует.</p>
        <p>IP: {client_ip}</p>
        <p>Время: {current_time}</p>
        <a href="/">Вернуться на главную</a>
        
        <h2>Журнал обращений:</h2>
        <ul>
            {"".join(f"<li>{log}</li>" for log in access_log[-10:])}
        </ul>
    </body>
</html>""", 404

@app.errorhandler(500)
def internal_error(err):
    return """<!doctype html>
<html>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <p>На сервере произошла непредвиденная ошибка.</p>
        <a href="/">Вернуться на главную</a>
    </body>
</html>""", 500

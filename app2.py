from flask import Flask
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3


app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)


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
                </ul>
            </nav>
        </main>
        <footer>
            Кучерова София Владимировна, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>"""


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
        <a href="/lab3/">Третья лабораторная</a>
    </div>
    
    <footer>
        &copy; София Кучерова, ФБИ-33, 2025
    </footer>
</body>
</html>

if name == "__main__":
    app.run(debug=True)'''
from flask import Blueprint, redirect, url_for

lab1= Blueprint('lab1',__name__)


@lab1.route("/")
@lab1.route("/index")
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

@lab1.route("/lab1")
def lab1():
    return """<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная работа 1</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
        Относится к категории так называемых микрофреймворков — минималистичных 
        каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        
        <a href="/">На главную</a>
        
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">WEB</a></li>
            <li><a href="/lab1/author">Автор</a></li>
            <li><a href="/lab1/image">Картинка</a></li>
            <li><a href="/lab1/counter">Счётчик</a></li>
            <li><a href="/lab1/info">Информация</a></li>
        </ul>
    </body>
</html>"""

@lab1.route("/lab1/web")
def web():
    headers = {
        'X-Server': 'Sophia Flask Server',
        'Content-Type': 'text/plain; charset=utf-8'
    }
    return """<!doctype html>
<html>
    <body>
        <h1>web-сервер на flask</h1>
        <a href="/lab1/author">Об авторе</a>
    </body>
</html>""", 200, headers

@lab1.route("/lab1/author")
def lab():
    name = "Кучерова София Владимировна"
    group = "ФБИ-33"
    faculty = "ФБ"
    return f"""<!doctype html>
<html>
    <body>
        <p>Студент: {name}</p>
        <p>Группа: {group}</p>
        <p>Факультет: {faculty}</p>
        <a href="/lab1/web">WEB</a>
    </body>
</html>"""

@lab1.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    return f"""<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{url_for('static', filename='lab1.css')}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="{path}" alt="Дуб">
    </body>
</html>"""

@lab1.route("/lab1/counter")
def counter():
    global count
    count += 1
    current_time = datetime.datetime.now()
    client_ip = request.remote_addr
    server_name = request.host
    
    return f"""<!doctype html>
<html>
    <body>
        <h1>Счётчик посещений</h1>
        <p>Сколько раз вы сюда заходили: {count}</p>
        <p>Текущая дата и время: {current_time}</p>
        <p>IP-адрес клиента: {client_ip}</p>
        <p>Имя хоста веб-сервера: {server_name}</p>
        <a href="/lab1/reset_counter">Сбросить счётчик</a>
    </body>
</html>"""

@lab1.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")





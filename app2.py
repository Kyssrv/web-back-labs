from flask import Flask, render_template, request, redirect, url_for, abort, make_response
import random

app = Flask(__name__)

# Счётчик посещений
counter = 0

# Главная страница и index
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Лабораторная 1
@app.route('/lab1')
def lab1():
    return render_template('lab1.html')

# Лабораторная 1 - Web
@app.route('/lab1/web')
def web():
    return render_template('web.html')

# Лабораторная 1 - Author
@app.route('/lab1/author')
def author():
    return render_template('author.html')

# Лабораторная 1 - Image
@app.route('/lab1/image')
def image():
    # Добавляем заголовки
    response = make_response(render_template('image.html'))
    response.headers['Content-Language'] = 'ru'
    response.headers['X-Custom-Header'] = 'MyCustomValue'
    response.headers['X-Developer'] = 'Student'
    return response

# Лабораторная 1 - Counter
@app.route('/lab1/counter')
def count():
    global counter
    counter += 1
    return render_template('counter.html', counter=counter)

# Лабораторная 1 - Очистка счётчика
@app.route('/lab1/counter/clear')
def clear_counter():
    global counter
    counter = 0
    return redirect(url_for('count'))

# Лабораторная 1 - Info
@app.route('/lab1/info')
def info():
    browser = request.user_agent.browser
    return render_template('info.html', browser=browser)

# Лабораторная 2
@app.route('/lab2')
def lab2():
    return render_template('lab2.html')

# Лабораторная 2 - База данных
@app.route('/lab2/database')
def database():
    return render_template('database.html')

# Лабораторная 2 - Запросы
@app.route('/lab2/queries')
def queries():
    return render_template('queries.html')

# Лабораторная 2 - Результаты
@app.route('/lab2/results')
def results():
    return render_template('results.html')

# Лабораторная 2 - Пример
@app.route('/lab2/example')
def example():
    name = 'София Кучерова'
    group = 'ФБИ-33'
    course = '2 курс'
    lab_number = 'Лабораторная работа 2'
    return render_template('example.html', 
                         name=name, 
                         group=group, 
                         course=course, 
                         lab_number=lab_number)

# Страницы с кодами ошибок
@app.route('/400')
def error_400():
    abort(400)

@app.route('/401')
def error_401():
    abort(401)

@app.route('/402')
def error_402():
    abort(402)

@app.route('/403')
def error_403():
    abort(403)

@app.route('/405')
def error_405():
    abort(405)

@app.route('/418')
def error_418():
    abort(418)

# Обработчик для ошибки 500 (вызов ошибки)
@app.route('/500')
def error_500():
    # Вызываем ошибку деления на ноль
    result = 10 / 0
    return str(result)

# Обработчики ошибок
@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400

@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401

@app.errorhandler(402)
def payment_required(error):
    return render_template('402.html'), 402

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405.html'), 405

@app.errorhandler(418)
def teapot(error):
    return render_template('418.html'), 418

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

@app.route('/lab2/example')
def example():
    name = 'София Кучерова'
    group = 'ФБИ-33'
    course = '3 курс'
    lab_num = 2
    
    # Список фруктов с ценами
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    
    # Список книг для дополнительного примера
    books = [
        {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
        {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Проза', 'pages': 320},
        {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
        {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
        {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
        {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
        {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
        {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160}
    ]
    
    return render_template('example.html', 
                         name=name, 
                         group=group, 
                         course=course, 
                         lab_num=lab_num,
                         fruits=fruits,
                         books=books)

# Лабораторная 2
@app.route('/lab2/')
def lab2():
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    
    return render_template('lab2.html', fruits=fruits)

if name == '__main__':
    app.run(debug=False)  # debug=False для тестирования ошибки 500
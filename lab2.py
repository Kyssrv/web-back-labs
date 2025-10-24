from flask import Blueprint, redirect, url_for

lab2= Blueprint('lab2',__name__)

@lab2.route("/lab2")
def lab2_main():
    return render_template('lab2.html')

@lab2.route("/lab2/example")
def example():
    name, lab_num, group, course = 'Кучерова София Владимировна', 2, 'ФБИ-33', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                         name=name, lab_num=lab_num, group=group,
                         course=course, fruits=fruits)

# Обработчики для работы с цветами
@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f"""<!doctype html>
<html>
    <body>
        <h1>Цветок #{flower_id}</h1>
        <p>Название: {flower_list[flower_id]}</p>
        <a href="/lab2/all_flowers">Все цветы</a>
    </body>
</html>"""

@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.lab2end(name)
    return f"""<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
        <a href="/lab2/all_flowers">Все цветы</a>
    </body>
</html>"""

@lab2.route('/lab2/all_flowers')
def all_flowers():
    flowers_html = ""
    for i, flower in enumerate(flower_list):
        flowers_html += f"<li>{i}. {flower} - <a href='/lab2/del_flower/{i}'>удалить</a></li>"
    
    return f"""<!doctype html>
<html>
    <body>
        <h1>Список цветов</h1>
        <ul>{flowers_html}</ul>
        
        <h2>Удалить все цветы</h2>
        <a href="/lab2/clear_flowers">Удалить все</a>
        
        <h2>Добавить цветок</h2>
        <form action="/lab2/add_flower_form" method="get">
            <input type="text" name="name" placeholder="Название цветка">
            <button type="submit">Добавить</button>
        </form>
    </body>
</html>"""

@lab2.route('/lab2/add_flower_form')
def add_flower_form():
    name = request.args.get('name', '')
    if name:
        flower_list.lab2end(name)
        return redirect('/lab2/all_flowers')
    else:
        return "Вы не задали имя цветка", 400

@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        removed_flower = flower_list.pop(flower_id)
        return redirect('/lab2/all_flowers')

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers')

# Калькулятор
@lab2.route('/lab2/calc')
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f"""<!doctype html>
<html>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <p>{a} + {b} = {a + b}</p>
        <p>{a} - {b} = {a - b}</p>
        <p>{a} × {b} = {a * b}</p>
        <p>{a} / {b} = {a / b if b != 0 else '∞'}</p>
        <p>{a}<sup>{b}</sup> = {a ** b}</p>
    </body>
</html>"""

# Фильтры
@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

# Слэши в адресах
@lab2.route('/lab2/a')
def a_without_slash():
    return 'ok - без слэша'

@lab2.route('/lab2/a/')
def a_with_slash():
    return 'ok - со слэшем'

if name == "__main__":
    lab2.run(debug=True)
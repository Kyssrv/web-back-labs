from flask import Blueprint, render_template, request, redirect, session

lab4 = Blueprint('lab4', __name__)
  
# Глобальная переменная для счетчика деревьев
tree_count = 0

# Существующие маршруты для арифметических операций
@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if not x1 or not x2:
        error = "Оба числа должны быть заполнены"
        return render_template('lab4/div-form.html', error=error)
    
    try:
        num1 = float(x1)
        num2 = float(x2)
        
        if num2 == 0:
            error = "Деление на ноль невозможно"
            return render_template('lab4/div-form.html', error=error)
        
        result = num1 / num2
        return render_template('lab4/div-form.html', 
                             x1=num1, x2=num2, result=result)
    
    except ValueError:
        error = "Введите корректные числа"
        return render_template('lab4/div-form.html', error=error)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    try:
        num1 = float(x1) if x1 else 0.0
        num2 = float(x2) if x2 else 0.0
        
        result = num1 + num2
        return render_template('lab4/sum-form.html', 
                             x1=num1, x2=num2, result=result)
    
    except ValueError:
        error = "Введите корректные числа"
        return render_template('lab4/sum-form.html', error=error)

@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')

@lab4.route('/lab4/mult', methods=['POST'])
def mult():
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')
    
    try:
        num1 = float(x1) if x1 else 1.0
        num2 = float(x2) if x2 else 1.0
        
        result = num1 * num2
        return render_template('lab4/mult-form.html', 
                             x1=num1, x2=num2, result=result)
    
    except ValueError:
        error = "Введите корректные числа"
        return render_template('lab4/mult-form.html', error=error)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if not x1 or not x2:
        error = "Оба числа должны быть заполнены"
        return render_template('lab4/sub-form.html', error=error)
    
    try:
        num1 = float(x1)
        num2 = float(x2)
        
        result = num1 - num2
        return render_template('lab4/sub-form.html', 
                             x1=num1, x2=num2, result=result)
    
    except ValueError:
        error = "Введите корректные числа"
        return render_template('lab4/sub-form.html', error=error)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if not x1 or not x2:
        error = "Оба числа должны быть заполнены"
        return render_template('lab4/pow-form.html', error=error)
    
    try:
        num1 = float(x1)
        num2 = float(x2)
        
        if num1 == 0 and num2 == 0:
            error = "Оба числа не могут быть равны нулю"
            return render_template('lab4/pow-form.html', error=error)
        
        result = num1 ** num2
        return render_template('lab4/pow-form.html', 
                             x1=num1, x2=num2, result=result)
    
    except ValueError:
        error = "Введите корректные числа"
        return render_template('lab4/pow-form.html', error=error)

# Новый маршрут для счетчика деревьев с валидацией
@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'GET':
        return render_template('lab4/tree.html', 
                             tree_count=tree_count,
                             can_plant=tree_count < 10,
                             can_cut=tree_count > 0)
    
    operation = request.form.get('operation')
    
    # Валидация на сервере
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1
    
    return redirect('/lab4/tree')

# Обновленный список пользователей с дополнительной информацией
users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Петров', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'male'},
    {'login': 'maria', 'password': 'qwerty', 'name': 'Мария Иванова', 'gender': 'female'},
    {'login': 'john', 'password': 'admin123', 'name': 'Джон Доу', 'gender': 'male'},
    {'login': 'anna', 'password': 'anna2024', 'name': 'Анна Сидорова', 'gender': 'female'}
]

# Роут для обработки запроса на адрес /lab4/login
@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab4/login.html', authorized=False)
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    # Сохраняем введенный логин для повторного заполнения поля
    saved_login = login or ''
    
    # Проверка на пустые значения
    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=saved_login)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=saved_login)
    
    # Поиск пользователя
    for user in users:
        if login == user['login'] and password == user['password']:
            return render_template('lab4/login.html', 
                                 name=user['name'], 
                                 authorized=True)
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=saved_login)

@lab4.route('/lab4/login', methods=['POST'])
def logout ():
    session.pop ('login', None)
    return redirect ('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temperature = request.form.get('temperature')
    
    # Проверка на пустое значение
    if not temperature:
        error = 'Ошибка: не задана температура'
        return render_template('lab4/fridge.html', error=error)
    
    try:
        temp = int(temperature)
    except ValueError:
        error = 'Ошибка: температура должна быть целым числом'
        return render_template('lab4/fridge.html', error=error)
    
    # Проверка диапазонов температуры
    if temp < -12:
        error = 'Не удалось установить температуру — слишком низкое значение'
        return render_template('lab4/fridge.html', error=error)
    
    if temp > -1:
        error = 'Не удалось установить температуру — слишком высокое значение'
        return render_template('lab4/fridge.html', error=error)
    
    # Определение количества снежинок
    if -12 <= temp <= -9:
        snowflakes = 3
    elif -8 <= temp <= -5:
        snowflakes = 2
    elif -4 <= temp <= -1:
        snowflakes = 1
    else:
        snowflakes = 0
    
    return render_template('lab4/fridge.html', 
                         temperature=temp, 
                         snowflakes=snowflakes, 
                         success=True)

@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/grain.html')
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    # Проверка на пустые значения
    if not grain_type:
        error = 'Не выбрано зерно'
        return render_template('lab4/grain.html', error=error)
    
    if not weight:
        error = 'Не указан вес'
        return render_template('lab4/grain.html', error=error)
    
    try:
        weight = float(weight)
    except ValueError:
        error = 'Вес должен быть числом'
        return render_template('lab4/grain.html', error=error)
    
    # Проверка веса на положительное значение
    if weight <= 0:
        error = 'Вес должен быть положительным числом'
        return render_template('lab4/grain.html', error=error)
    
    # Проверка на максимальный объем
    if weight > 100:
        error = 'Такого объёма сейчас нет в наличии'
        return render_template('lab4/grain.html', error=error)
    
    # Цены за тонну
    prices = {
        'barley': 12000,  # ячмень
        'oats': 8500,     # овёс
        'wheat': 9000,    # пшеница
        'rye': 15000      # рожь
    }
    
    # Названия зерна для вывода
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    price_per_ton = prices[grain_type]
    total = weight * price_per_ton
    discount = 0
    discount_applied = False
    
    # Применение скидки за большой объем
    if weight > 10:
        discount = total * 0.1
        total -= discount
        discount_applied = True
    
    return render_template('lab4/grain.html', 
                         success=True,
                         grain_name=grain_names[grain_type],
                         weight=weight,
                         total=total,
                         discount_applied=discount_applied,
                         discount=discount)
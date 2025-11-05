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

# Добавляем пользователей в список
users = [
    {'login': 'alex', 'password': 123},
    {'login': 'bob', 'password': 555},
    {'login': 'maria', 'password': 'qwerty'},  # Добавленный пользователь
    {'login': 'john', 'password': 'admin123'}   # Добавленный пользователь
]

# Роут для обработки запроса на адрес /lab4/login
@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
       if 'login' in session:
           authorized= True
           login =session ['login']
        else:
            authorized= False
            login=''
        return render_template('lab4/login.html', authorized=authorized, login=login)
    
    login = request.form.get('login')
    password = request.form.get('password')  

    for user in users:
        # Сравниваем логин и пароль (приводим к строке для единообразия)
        if login == user['login'] and str(password) == str(user['password']):
            session['login']=login
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False)

@lab4.route('/lab4/login', methods=['POST'])
def logout ():
    session.pop ('login', None)
    return redirect ('/lab4/login')
from flask import Blueprint, render_template, request, make_response, redirect, url_for

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color', '#000000')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(render_template('lab3/cookie.html'))
    resp.set_cookie('name', 'Ваше Имя', max_age=3600)
    resp.set_cookie('name_color', '#ff0000', max_age=3600)
    return resp

@lab3.route('/lab3/clear-cookies')
def clear_cookies():
    resp = make_response(redirect(url_for('lab3.lab')))
    resp.delete_cookie('name')
    resp.delete_cookie('name_color')
    resp.delete_cookie('age')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    
    if user == '':
        errors['user'] = 'Заполните поле!'
    
    if age == '':
        errors['age'] = 'Заполните поле!'
    
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/ticket')
def ticket_form():
    errors = {}
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    return render_template('lab3/ticket_form.html', 
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, errors=errors)

@lab3.route('/lab3/ticket_result')
def ticket_result():
    errors = {}
    
    # Получаем данные из формы
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age_str = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    # Валидация
    if not fio:
        errors['fio'] = 'Заполните поле ФИО'
    if not shelf:
        errors['shelf'] = 'Выберите тип полки'
    if not age_str:
        errors['age'] = 'Заполните поле возраста'
    elif not age_str.isdigit() or not (1 <= int(age_str) <= 120):
        errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    if not departure:
        errors['departure'] = 'Заполните пункт выезда'
    if not destination:
        errors['destination'] = 'Заполните пункт назначения'
    if not date:
        errors['date'] = 'Выберите дату поездки'
    
    # Если есть ошибки, показываем форму снова
    if errors:
        return render_template('lab3/ticket_form.html', 
                             fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                             age=age_str, departure=departure, destination=destination,
                             date=date, insurance=insurance, errors=errors)
    
    # Расчет стоимости
    age = int(age_str)
    if age < 18:
        price = 700  # Детский билет
    else:
        price = 1000  # Взрослый билет
    
    # Доплаты
    if shelf in ['lower', 'lower-side']:
        price += 100  # Нижняя или нижняя боковая полка
    
    if linen == 'on':
        price += 75  # Бельё
    
    if luggage == 'on':
        price += 250  # Багаж
    
    if insurance == 'on':
        price += 150  # Страховка
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, price=price)

@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        username = request.form.get('username')
        color = request.form.get('color')
        age = request.form.get('age')
        
        resp = make_response(redirect(url_for('lab3.lab')))
        if username:
            resp.set_cookie('name', username, max_age=3600)
        if color:
            resp.set_cookie('name_color', color, max_age=3600)
        if age:
            resp.set_cookie('age', age, max_age=3600)
        
        return resp
    
    username = request.cookies.get('name')
    color = request.cookies.get('name_color', '#000000')
    age = request.cookies.get('age')
    
    return render_template('lab3/settings.html', username=username, color=color, age=age)

@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect(url_for('lab3.settings')))
    resp.delete_cookie('name')
    resp.delete_cookie('name_color')
    resp.delete_cookie('age')
    return resp

from flask import Blueprint, render_template, request, make_response, redirect, url_for

lab3 = Blueprint('lab3', __name__)

# Список товаров
PRODUCTS = [
    {"name": "iPhone 14", "price": 79990, "brand": "Apple", "color": "Черный", "weight": 172, "category": "Смартфон"},
    {"name": "Samsung Galaxy S23", "price": 69990, "brand": "Samsung", "color": "Белый", "weight": 168, "category": "Смартфон"},
    {"name": "Xiaomi Redmi Note 12", "price": 24990, "brand": "Xiaomi", "color": "Синий", "weight": 183, "category": "Смартфон"},
    {"name": "MacBook Air M2", "price": 129990, "brand": "Apple", "color": "Серебристый", "weight": 1240, "category": "Ноутбук"},
    {"name": "Asus ROG Strix", "price": 159990, "brand": "Asus", "color": "Черный", "weight": 2500, "category": "Ноутбук"},
    {"name": "Lenovo IdeaPad", "price": 45990, "brand": "Lenovo", "color": "Серый", "weight": 1600, "category": "Ноутбук"},
    {"name": "iPad Air", "price": 59990, "brand": "Apple", "color": "Розовый", "weight": 461, "category": "Планшет"},
    {"name": "Samsung Tab S8", "price": 54990, "brand": "Samsung", "color": "Серебристый", "weight": 503, "category": "Планшет"},
    {"name": "AirPods Pro", "price": 24990, "brand": "Apple", "color": "Белый", "weight": 45, "category": "Наушники"},
    {"name": "Sony WH-1000XM4", "price": 29990, "brand": "Sony", "color": "Черный", "weight": 254, "category": "Наушники"},
    {"name": "Apple Watch Series 8", "price": 39990, "brand": "Apple", "color": "Золотой", "weight": 42, "category": "Смарт-часы"},
    {"name": "Samsung Galaxy Watch", "price": 19990, "brand": "Samsung", "color": "Серебристый", "weight": 49, "category": "Смарт-часы"},
    {"name": "PlayStation 5", "price": 59990, "brand": "Sony", "color": "Белый", "weight": 4500, "category": "Консоль"},
    {"name": "Xbox Series X", "price": 49990, "brand": "Microsoft", "color": "Черный", "weight": 4400, "category": "Консоль"},
    {"name": "Nintendo Switch", "price": 29990, "brand": "Nintendo", "color": "Синий-Красный", "weight": 398, "category": "Консоль"},
    {"name": "Canon EOS R6", "price": 189990, "brand": "Canon", "color": "Черный", "weight": 680, "category": "Фотоаппарат"},
    {"name": "Sony A7 III", "price": 159990, "brand": "Sony", "color": "Черный", "weight": 650, "category": "Фотоаппарат"},
    {"name": "GoPro Hero 11", "price": 34990, "brand": "GoPro", "color": "Черный", "weight": 153, "category": "Экшн-камера"},
    {"name": "Kindle Paperwhite", "price": 12990, "brand": "Amazon", "color": "Черный", "weight": 205, "category": "Электронная книга"},
    {"name": "DJI Mini 3 Pro", "price": 79990, "brand": "DJI", "color": "Серый", "weight": 249, "category": "Дрон"},
    {"name": "JBL Flip 6", "price": 8990, "brand": "JBL", "color": "Синий", "weight": 550, "category": "Колонка"},
    {"name": "Logitech MX Master", "price": 8990, "brand": "Logitech", "color": "Графитовый", "weight": 145, "category": "Мышь"},
    {"name": "Razer BlackWidow", "price": 12990, "brand": "Razer", "color": "Черный", "weight": 1040, "category": "Клавиатура"},
    {"name": "WD My Passport", "price": 4990, "brand": "Western Digital", "color": "Красный", "weight": 130, "category": "Внешний диск"}
]

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
    

@lab3.route('/lab3/products')
def products():
    # Получаем цены из куки или из запроса
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    min_price = request.args.get('min_price', min_price_cookie)
    max_price = request.args.get('max_price', max_price_cookie)
    
    # Обработка сброса
    if request.args.get('reset') == 'true':
        min_price = ''
        max_price = ''
    
    # Рассчитываем минимальную и максимальную цену среди всех товаров
    all_prices = [product['price'] for product in PRODUCTS]
    min_product_price = min(all_prices)
    max_product_price = max(all_prices)
    
    # Фильтрация товаров
    filtered_products = PRODUCTS
    searched = False
    
    if min_price or max_price:
        searched = True
    
    # Преобразуем в числа, если указаны
        try:
            min_val = float(min_price) if min_price else min_product_price
            max_val = float(max_price) if max_price else max_product_price
        except (ValueError, TypeError):
            min_val = min_product_price
            max_val = max_product_price
        
        # Автоматическое исправление, если min > max
        if min_val > max_val:
            min_val, max_val = max_val, min_val
            # Меняем местами значения для отображения в форме
            min_price, max_price = max_price, min_price
        
        # Фильтруем товары
        filtered_products = [
            product for product in PRODUCTS
            if min_val <= product['price'] <= max_val
        ]
    
    # Создаем ответ
    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered_products,
        min_price=min_price,
        max_price=max_price,
        min_product_price=min_product_price,
        max_product_price=max_product_price,
        searched=searched
    ))
    
    # Сохраняем значения в куки (если не сброс)
    if request.args.get('reset') != 'true':
        if min_price:
            resp.set_cookie('min_price', min_price, max_age=30*24*3600)  # 30 дней
        else:
            resp.delete_cookie('min_price')
        
        if max_price:
            resp.set_cookie('max_price', max_price, max_age=30*24*3600)  # 30 дней
        else:
            resp.delete_cookie('max_price')
    else:
        # Очищаем куки при сбросе
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
    
    return resp
from flask import Blueprint, render_template, request, make_response, redirect, url_for

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color', '#000000')
    return render_template('lab3/lab3.html', name=name, name_color=name_color)

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
    
    # Пусть кофе стоит 120 рублей, чёрный чай — 80 рублей, зелёный — 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    # Добавка молока удорожает напиток на 30 рублей, а сахара — на 10.
    if request.args.get('milk') == 'on':
        price += 30
    
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)
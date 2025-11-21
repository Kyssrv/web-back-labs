from flask import Blueprint, render_template, session, request, redirect, url_for

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5')
def main():
    username = session.get('login', 'anonymous')
    return render_template('lab5/lab5.html', username=username)

@lab5.route('/lab5/login')
def login():
    return "Страница входа - будет реализована позже"

@lab5.route('/lab5/register')
def register():
    return "Страница регистрации - будет реализована позже"

@lab5.route('/lab5/list')
def list_articles():
    return "Список статей - будет реализован позже"

@lab5.route('/lab5/create')
def create():
    return "Создание статьи - будет реализовано позже"
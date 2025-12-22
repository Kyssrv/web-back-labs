from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящим по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора». Каждый из узников которого однажды проходит зелёную милю..."
    }
]

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

# Получение всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

# Получение одного фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return {'error': 'Фильм не найден'}, 404
    return jsonify(films[id])

# Удаление фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return {'error': 'Фильм не найден'}, 404
    del films[id]
    return '', 204

# Редактирование фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return {'error': 'Фильм не найден'}, 404
    
    film = request.get_json()
    
    # ЗАДАНИЕ 2: Если оригинальное название пустое, а русское задано - копируем русское
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']
    
    # Валидация
    if not film.get('title_ru', '').strip():
        return {'title_ru': 'Русское название обязательно'}, 400
    
    if film.get('description', '').strip() == '':
        return {'description': 'Заполните описание'}, 400
    
    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > 2025:
            return {'year': 'Год должен быть от 1895 до 2025'}, 400
    except ValueError:
        return {'year': 'Год должен быть числом'}, 400
    
    films[id] = film
    return jsonify(films[id])

# Добавление нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    # ЗАДАНИЕ 2: Если оригинальное название пустое, а русское задано - копируем русское
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']
    
    # Валидация
    if not film.get('title_ru', '').strip():
        return {'title_ru': 'Русское название обязательно'}, 400
    
    if film.get('description', '').strip() == '':
        return {'description': 'Заполните описание'}, 400
    
    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > 2025:
            return {'year': 'Год должен быть от 1895 до 2025'}, 400
    except ValueError:
        return {'year': 'Год должен быть числом'}, 400
    
    films.append(film)
    return jsonify({'id': len(films) - 1})
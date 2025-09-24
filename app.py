from flask import Flask

app = Flask(__name__)

# Переносим стартовую точку на /web и добавляем ссылку на автора
@app.route("/web")
def web():
    return f"""<!DOCTYPE html>
        <html lang="en">
          <head>
              <meta charset="UTF-8"/>
              <title>Web Server on Flask</title>
          </head>
          <body>
              <h1>Web-сервер на Flask</h1>
              <!-- Добавили ссылку на автора -->
              <a href="/author">Автор</a>
          </body>
        </html>"""

# Оставляем неизменённым обработчик /author
@app.route("/author")
def author():
    name = "Кучерова София Владимировна"
    group = "ФБИ-33"
    faculty = "ФБ"
    
    return f"""<!DOCTYPE html>
        <html lang="en">
          <head>
              <meta charset="UTF-8"/>
              <title>Автор проекта</title>
          </head>
          <body>
              <p>Студент: {name}</p>
              <p>Группа: {group}</p>
              <p>Факультет: {faculty}</p>
              <!-- Добавили обратную ссылку на основную страницу -->
              <a href="/web">Вернуться назад</a>
          </body>
        </html>"""

if __name__ == "__main__":
    app.run(debug=True)

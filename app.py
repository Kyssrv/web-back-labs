from flask import Flask, url_for, request, redirect
import datatime

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

@app.route('/image')
def image():
    path=url_for("static", filename="дуб.jpg")
    return'''
<!doctype html>
<html>
    <body>
        <h1>Дуб</h1>
        <img src="'''+ path +'''">
    </body>
</html>
'''
count=0

@app.route('/counter')
def counter():
    count+=1
    time=datatime.datetime.today()
    url=request.url
    client_ip=request.remote_addr
    return'''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: '''+str(count)+'''
        <hr>
        Дата и время: '''+time+'''<br>
        Запрошенный адрес: '''+url+'''<br>
        Ваш IP адрес: '''+client_ip+'''<br>
    </body>
</html>
'''
@app.route("/into")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return'''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
'''


if __name__ == "__main__":
    app.run(debug=True)

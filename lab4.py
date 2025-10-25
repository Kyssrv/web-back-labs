rom flask import Blueprint, render_template, request

lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    # Получаем данные из формы
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    # Проверяем, что оба числа были введены
    if not x1 or not x2:
        error = "Оба числа должны быть заполнены"
        return render_template('lab4/div-form.html', error=error)
    
    try:
        # Преобразуем в числа
        num1 = float(x1)
        num2 = float(x2)
        
        # Проверяем деление на ноль
        if num2 == 0:
            error = "Деление на ноль невозможно"
            return render_template('lab4/div-form.html', error=error)
        
        # Выполняем деление
        result = num1 / num2
        
        # Возвращаем результат
        return render_template('lab4/div-form.html', 
                             x1=num1, x2=num2, result=result)
    
    except ValueError:
        error = "Введите корректные числа"
        return render_template('lab4/div-form.html', error=error)
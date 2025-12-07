from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

offices = []
for i in range(1, 11):
    # Разная стоимость аренды: чем выше номер офиса, тем дороже
    price = 800 + 150 * i  # Цены от 950 до 2300 руб.
    offices.append({"number": i, "tenant": "", "price": price})

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    login = session.get('login')  # Получаем логин из сессии
    
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    if data['method'] == 'booking':
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Not authorized'
                },
                'id': id
            }
        
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': offices,
                    'id': id
                }
    
    if data['method'] == 'cancellation':
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Not authorized'
                },
                'id': id
            }
        
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not rented'
                        },
                        'id': id
                    }
                
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel another user\'s rental'
                        },
                        'id': id
                    }
                
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': offices,
                    'id': id
                }
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
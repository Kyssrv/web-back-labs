from flask import Blueprint, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

lab6 = Blueprint('lab6', __name__)

# Инициализация базы данных (убедитесь, что db создана в основном файле приложения)
from app import db

# Модель Office
class Office(db.Model):
    __tablename__ = 'offices'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    tenant = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'number': self.number,
            'tenant': self.tenant if self.tenant else '',
            'price': self.price
        }

@lab6.route('/lab6/')
def main():
    return render_template('lab6.html')

@lab6.route('/lab6/init-db/')
def init_db():
    """Эндпоинт для инициализации базы данных (вызывается один раз)"""
    try:
        # Создаем таблицу, если она не существует
        db.create_all()
        
        # Очищаем таблицу
        Office.query.delete()
        
        # Добавляем начальные данные
        offices_data = []
        for i in range(1, 11):
            price = 800 + 150 * i
            offices_data.append(Office(number=i, tenant='', price=price))
        
        db.session.bulk_save_objects(offices_data)
        db.session.commit()
        
        return 'База данных инициализирована успешно!'
    except Exception as e:
        db.session.rollback()
        return f'Ошибка: {str(e)}'

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    login = session.get('login', '')  # Получаем логин из сессии
    
    if data['method'] == 'info':
        try:
            # Получаем все офисы из базы данных
            offices = Office.query.order_by(Office.number).all()
            offices_list = [office.to_dict() for office in offices]
            
            return {
                'jsonrpc': '2.0',
                'result': offices_list,
                'id': id
            }
        except Exception as e:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'message': f'Database error: {str(e)}'
                },
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
        try:
            # Находим офис в базе данных
            office = Office.query.filter_by(number=office_number).first()
            
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 404,
                        'message': 'Office not found'
                    },
                    'id': id
                }
            
            if office.tenant:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Already booked'
                    },
                    'id': id
                }
            
            # Обновляем арендатора
            office.tenant = login
            db.session.commit()
            
            # Получаем обновленный список
            offices = Office.query.order_by(Office.number).all()
            offices_list = [office.to_dict() for office in offices]
            
            return {
                'jsonrpc': '2.0',
                'result': offices_list,
                'id': id
            }
        except Exception as e:
            db.session.rollback()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'message': f'Database error: {str(e)}'
                },
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
        try:
            # Находим офис в базе данных
            office = Office.query.filter_by(number=office_number).first()
            
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 404,
                        'message': 'Office not found'
                    },
                    'id': id
                }
            
            if not office.tenant:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Office is not rented'
                    },
                    'id': id
                }
            
            if office.tenant != login:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 4,
                        'message': 'Cannot cancel another user\'s rental'
                    },
                    'id': id
                }
            
            # Освобождаем офис
            office.tenant = None
            db.session.commit()
            
            # Получаем обновленный список
            offices = Office.query.order_by(Office.number).all()
            offices_list = [office.to_dict() for office in offices]
            
            return {
                'jsonrpc': '2.0',
                'result': offices_list,
                'id': id
            }
        except Exception as e:
            db.session.rollback()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'message': f'Database error: {str(e)}'
                },
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
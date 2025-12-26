from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from db import db
from db.models import users, articles
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import desc, or_, func
from datetime import datetime

lab8 = Blueprint('lab8', __name__, template_folder='templates/lab8')

# ==================== ГЛАВНАЯ СТРАНИЦА ====================
@lab8.route('/lab8/')
def index():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    
    # Получаем последние публичные статьи для главной (ДЛЯ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ)
    latest_articles = articles.query.filter_by(is_public=True)\
        .order_by(desc(articles.created_at))\
        .limit(6)\
        .all()
    
    # Получаем самые популярные статьи (по лайкам)
    popular_articles = articles.query.filter_by(is_public=True)\
        .order_by(desc(articles.likes))\
        .limit(3)\
        .all()
    
    return render_template('index.html', 
                         username=username,
                         latest_articles=latest_articles,
                         popular_articles=popular_articles)

# ==================== СПИСОК ВСЕХ ПУБЛИЧНЫХ СТАТЕЙ ====================
@lab8.route('/lab8/articles/public')
def public_articles():
    """Страница со всеми публичными статьями (доступна всем)"""
    
    # Получаем параметры пагинации
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Запрос для публичных статей с пагинацией
    public_query = articles.query.filter_by(is_public=True)\
        .order_by(desc(articles.created_at))
    
    # Пагинация
    pagination = public_query.paginate(page=page, per_page=per_page, error_out=False)
    public_articles_list = pagination.items
    
    # Статистика
    total_public = articles.query.filter_by(is_public=True).count()
    
    return render_template('articles/public.html',
                         public_articles=public_articles_list,
                         pagination=pagination,
                         total_public=total_public)

# ==================== ПОИСК ПО СТАТЬЯМ ====================
@lab8.route('/lab8/articles/search')
def search_articles():
    """Поиск по статьям (регистронезависимый)"""
    
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all')  # all, public, my
    
    if not query:
        flash('Введите поисковый запрос', 'info')
        return redirect(request.referrer or url_for('lab8.index'))
    
    # Регистронезависимый поиск
    search_pattern = f'%{query}%'
    
    # Собираем результаты поиска
    results = []
    search_title = f'Результаты поиска: "{query}"'
    
    if search_type == 'all' or not current_user.is_authenticated:
        # Ищем в публичных статьях (для всех)
        public_results = articles.query.filter(
            articles.is_public == True,
            or_(
                func.lower(articles.title).like(func.lower(search_pattern)),
                func.lower(articles.article_text).like(func.lower(search_pattern))
            )
        ).order_by(desc(articles.created_at)).all()
        results.extend(public_results)
        
        if not current_user.is_authenticated:
            search_title = f'Публичные статьи по запросу: "{query}"'
    
    if current_user.is_authenticated and (search_type == 'all' or search_type == 'my'):
        # Ищем в своих статьях (даже приватных)
        my_results = articles.query.filter(
            articles.login_id == current_user.id,
            or_(
                func.lower(articles.title).like(func.lower(search_pattern)),
                func.lower(articles.article_text).like(func.lower(search_pattern))
            )
        ).order_by(desc(articles.created_at)).all()
        
        # Добавляем только те, которых еще нет в результатах
        for article in my_results:
            if article not in results:
                results.append(article)
        
        if search_type == 'my':
            search_title = f'Мои статьи по запросу: "{query}"'
    
    # Убираем дубликаты
    unique_results = []
    seen_ids = set()
    for article in results:
        if article.id not in seen_ids:
            seen_ids.add(article.id)
            unique_results.append(article)
    
    return render_template('articles/search.html',
                         query=query,
                         articles=unique_results,
                         search_type=search_type,
                         search_title=search_title,
                         results_count=len(unique_results))

# ==================== АВТОРЫ СТАТЕЙ ====================
@lab8.route('/lab8/articles/authors')
def article_authors():
    """Список авторов публичных статей"""
    
    # Получаем уникальных авторов публичных статей
    authors = users.query.join(articles)\
        .filter(articles.is_public == True)\
        .group_by(users.id)\
        .order_by(users.login)\
        .all()
    
    # Для каждого автора считаем количество публичных статей
    authors_with_stats = []
    for author in authors:
        article_count = articles.query.filter_by(
            login_id=author.id,
            is_public=True
        ).count()
        
        # Получаем последнюю статью автора
        latest_article = articles.query.filter_by(
            login_id=author.id,
            is_public=True
        ).order_by(desc(articles.created_at)).first()
        
        authors_with_stats.append({
            'author': author,
            'article_count': article_count,
            'latest_article': latest_article
        })
    
    return render_template('articles/authors.html',
                         authors=authors_with_stats)

# ==================== СТАТЬИ КОНКРЕТНОГО АВТОРА ====================
@lab8.route('/lab8/articles/author/<int:author_id>')
def author_articles(author_id):
    """Публичные статьи конкретного автора"""
    
    author = users.query.get_or_404(author_id)
    
    # Получаем публичные статьи автора
    author_articles_list = articles.query.filter(
        articles.login_id == author_id,
        articles.is_public == True
    ).order_by(desc(articles.created_at)).all()
    
    # Статистика автора
    total_articles = articles.query.filter_by(login_id=author_id, is_public=True).count()
    
    return render_template('articles/author_detail.html',
                         author=author,
                         articles=author_articles_list,
                         total_articles=total_articles)

# ==================== ОБНОВЛЕННЫЙ СПИСОК СТАТЕЙ ====================
@lab8.route('/lab8/articles/')
@login_required
def article_list():
    """Список статей пользователя (только для авторизованных)"""
    
    # Фильтры
    filter_type = request.args.get('filter', 'all')  # all, public, private, favorite
    
    # Базовый запрос для статей пользователя
    query = articles.query.filter_by(login_id=current_user.id)
    
    # Применяем фильтры
    if filter_type == 'public':
        query = query.filter_by(is_public=True)
    elif filter_type == 'private':
        query = query.filter_by(is_public=False)
    elif filter_type == 'favorite':
        query = query.filter_by(is_favorite=True)
    
    user_articles = query.order_by(desc(articles.created_at)).all()
    
    # Статистика
    stats = {
        'all': articles.query.filter_by(login_id=current_user.id).count(),
        'public': articles.query.filter_by(login_id=current_user.id, is_public=True).count(),
        'private': articles.query.filter_by(login_id=current_user.id, is_public=False).count(),
        'favorite': articles.query.filter_by(login_id=current_user.id, is_favorite=True).count()
    }
    
    return render_template('articles/list.html',
                         user_articles=user_articles,
                         filter_type=filter_type,
                         stats=stats)

# ==================== ОБНОВЛЕННОЕ СОЗДАНИЕ СТАТЬИ ====================
@lab8.route('/lab8/articles/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('articles/create.html')
    
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_public = 'is_public' in request.form
    is_favorite = 'is_favorite' in request.form
    
    errors = []
    if not title:
        errors.append('Заголовок обязателен')
    elif len(title) > 100:
        errors.append('Заголовок не должен превышать 100 символов')
    
    if not article_text:
        errors.append('Текст статьи обязателен')
    elif len(article_text) > 10000:
        errors.append('Текст статьи не должен превышать 10000 символов')
    
    if errors:
        return render_template('articles/create.html',
                             errors=errors,
                             title=title,
                             article_text=article_text,
                             is_public=is_public,
                             is_favorite=is_favorite)
    
    try:
        new_article = articles(
            login_id=current_user.id,
            title=title,
            article_text=article_text,
            is_public=is_public,
            is_favorite=is_favorite,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_article)
        db.session.commit()
        
        flash('Статья успешно создана!', 'success')
        return redirect(f'/lab8/articles/{new_article.id}')
    
    except Exception as e:
        db.session.rollback()
        return render_template('articles/create.html',
                             errors=[f'Ошибка при создании статьи: {str(e)}'],
                             title=title,
                             article_text=article_text,
                             is_public=is_public,
                             is_favorite=is_favorite)

# ==================== API ДЛЯ ПОИСКА (AJAX) ====================
@lab8.route('/lab8/api/search')
def api_search():
    """API для быстрого поиска (AJAX)"""
    
    query = request.args.get('q', '').strip()
    limit = request.args.get('limit', 5, type=int)
    
    if not query or len(query) < 2:
        return jsonify({'success': False, 'error': 'Слишком короткий запрос'})
    
    search_pattern = f'%{query}%'
    
    results = []
    
    # Публичные статьи (для всех)
    public_results = articles.query.filter(
        articles.is_public == True,
        or_(
            func.lower(articles.title).like(func.lower(search_pattern)),
            func.lower(articles.article_text).like(func.lower(search_pattern))
        )
    ).limit(limit).all()
    
    for article in public_results:
        results.append({
            'id': article.id,
            'title': article.title,
            'author': article.author.login,
            'excerpt': article.article_text[:100] + '...' if len(article.article_text) > 100 else article.article_text,
            'url': url_for('lab8.article_detail', article_id=article.id),
            'type': 'public'
        })
    
    # Свои статьи (если авторизован)
    if current_user.is_authenticated:
        my_results = articles.query.filter(
            articles.login_id == current_user.id,
            or_(
                func.lower(articles.title).like(func.lower(search_pattern)),
                func.lower(articles.article_text).like(func.lower(search_pattern))
            )
        ).limit(limit).all()
        
        for article in my_results:
            # Проверяем, нет ли уже этой статьи в результатах
            if not any(r['id'] == article.id for r in results):
                results.append({
                    'id': article.id,
                    'title': article.title,
                    'author': 'Вы',
                    'excerpt': article.article_text[:100] + '...' if len(article.article_text) > 100 else article.article_text,
                    'url': url_for('lab8.article_detail', article_id=article.id),
                    'type': 'my' if not article.is_public else 'my_public'
                })
    
    return jsonify({
        'success': True,
        'query': query,
        'results': results[:limit],  # Ограничиваем общее количество
        'count': len(results)
    })

# ==================== ДОБАВЛЕНИЕ/УДАЛЕНИЕ ЛАЙКОВ ====================
@lab8.route('/lab8/articles/<int:article_id>/like', methods=['POST'])
def like_article(article_id):
    """Добавление лайка к публичной статье"""
    
    article = articles.query.get_or_404(article_id)
    
    # Проверяем, что статья публичная
    if not article.is_public:
        return jsonify({'success': False, 'error': 'Статья не публичная'}), 403
    
    try:
        article.likes = (article.likes or 0) + 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'likes': article.likes,
            'message': 'Спасибо за лайк!'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== СТАТИСТИКА САЙТА ====================
@lab8.route('/lab8/stats')
def site_stats():
    """Общая статистика сайта"""
    
    total_articles = articles.query.count()
    public_articles = articles.query.filter_by(is_public=True).count()
    total_authors = users.query.count()
    active_authors = users.query.join(articles)\
        .filter(articles.is_public == True)\
        .group_by(users.id)\
        .count()
    
    # Самые популярные статьи
    top_articles = articles.query.filter_by(is_public=True)\
        .order_by(desc(articles.likes))\
        .limit(5)\
        .all()
    
    # Самые активные авторы
    top_authors = users.query\
        .join(articles)\
        .filter(articles.is_public == True)\
        .group_by(users.id)\
        .order_by(func.count(articles.id).desc())\
        .limit(5)\
        .all()
    
    # Для каждого топ-автора считаем количество статей
    top_authors_with_counts = []
    for author in top_authors:
        count = articles.query.filter_by(
            login_id=author.id,
            is_public=True
        ).count()
        top_authors_with_counts.append({'author': author, 'count': count})
    
    return render_template('stats.html',
                         total_articles=total_articles,
                         public_articles=public_articles,
                         total_authors=total_authors,
                         active_authors=active_authors,
                         top_articles=top_articles,
                         top_authors=top_authors_with_counts)
// Заполнение таблицы фильмами
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function(data) {
            return data.json();
        })
        .then(function(films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            for(let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');
                
                // ЗАДАНИЕ 3: Поменяли местами ячейки
                
                // Ячейка для русского названия
                let tdTitleRus = document.createElement('td');
                tdTitleRus.innerHTML = `<span class="russian-title">${films[i].title_ru}</span>`;
                
                // Ячейка для оригинального названия
                let tdTitle = document.createElement('td');
                if (films[i].title && films[i].title !== films[i].title_ru) {
                    // ЗАДАНИЕ 3: Оригинальное название курсивом
                    tdTitle.innerHTML = `<div class="original-title">(${films[i].title})</div>`;
                } else {
                    tdTitle.innerHTML = '<div class="original-title" style="color: #aaa;">(без оригинального названия)</div>';
                }
                
                let tdYear = document.createElement('td');
                tdYear.innerHTML = `<strong>${films[i].year}</strong>`;
                
                let tdActions = document.createElement('td');
                
                // Кнопка редактирования
                let editButton = document.createElement('button');
                editButton.className = 'edit-btn';
                editButton.innerHTML = '✏️ Редактировать';
                editButton.onclick = function() {
                    editFilm(i);
                };
                
                // Кнопка удаления
                let delButton = document.createElement('button');
                delButton.className = 'delete-btn';
                delButton.innerHTML = '🗑️ Удалить';
                delButton.onclick = function() {
                    deleteFilm(i, films[i].title_ru);
                };
                
                tdActions.append(editButton);
                tdActions.append(delButton);
                
                tr.append(tdTitleRus); // Сначала русское название
                tr.append(tdTitle);    // Затем оригинальное
                tr.append(tdYear);
                tr.append(tdActions);
                
                tbody.append(tr);
            }
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке фильмов:', error);
        });
}

// Удаление фильма
function deleteFilm(id, title) {
    if(!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function() {
            fillFilmList();
            showNotification('Фильм успешно удалён!', 'success');
        })
        .catch(function(error) {
            showNotification('Ошибка при удалении фильма', 'error');
        });
}

// Показ уведомления
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 9999;
        animation: slideInRight 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    if (type === 'success') {
        notification.style.backgroundColor = '#2ecc71';
    } else {
        notification.style.backgroundColor = '#e74c3c';
    }
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Показ модального окна
function showModal(title = 'Добавление фильма') {
    document.getElementById('modalTitle').textContent = title;
    clearErrors();
    document.getElementById('filmModal').style.display = 'block';
}

// Скрытие модального окна
function hideModal() {
    document.getElementById('filmModal').style.display = 'none';
}

// Отмена редактирования/добавления
function cancel() {
    hideModal();
}

// Очистка ошибок
function clearErrors() {
    document.getElementById('title_ru_error').textContent = '';
    document.getElementById('title_error').textContent = '';
    document.getElementById('year_error').textContent = '';
    document.getElementById('description_error').textContent = '';
    
    document.getElementById('title_ru').classList.remove('error-field');
    document.getElementById('title').classList.remove('error-field');
    document.getElementById('year').classList.remove('error-field');
    document.getElementById('description').classList.remove('error-field');
}

// Добавление нового фильма
function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('title').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal('Добавление фильма');
}

// Редактирование фильма
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function(data) {
            return data.json();
        })
        .then(function(film) {
            document.getElementById('id').value = id;
            document.getElementById('title_ru').value = film.title_ru;
            document.getElementById('title').value = film.title;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal('Редактирование фильма');
        })
        .catch(function(error) {
            showNotification('Ошибка при загрузке фильма', 'error');
        });
}

// Отправка фильма (добавление или редактирование)
function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title_ru').value.trim(),
        year: document.getElementById('year').value.trim(),
        description: document.getElementById('description').value.trim()
    };
    
    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';
    
    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            return resp.json().then(function(data) {
                fillFilmList();
                hideModal();
                showNotification(id === '' ? 'Фильм успешно добавлен!' : 'Фильм успешно обновлён!', 'success');
                return {};
            });
        }
        return resp.json().then(function(errors) {
            return {errors: errors, status: resp.status};
        });
    })
    .then(function(result) {
        if(result.errors) {
            // Отображение ошибок валидации
            clearErrors();
            
            if(result.errors.title_ru) {
                document.getElementById('title_ru_error').textContent = result.errors.title_ru;
                document.getElementById('title_ru').classList.add('error-field');
            }
            
            if(result.errors.year) {
                document.getElementById('year_error').textContent = result.errors.year;
                document.getElementById('year').classList.add('error-field');
            }
            
            if(result.errors.description) {
                document.getElementById('description_error').textContent = result.errors.description;
                document.getElementById('description').classList.add('error-field');
            }
            
            if(result.errors.title) {
                document.getElementById('title_error').textContent = result.errors.title;
                document.getElementById('title').classList.add('error-field');
            }
        }
    })
    .catch(function(error) {
        showNotification('Ошибка при сохранении фильма', 'error');
        console.error('Ошибка:', error);
    });
}
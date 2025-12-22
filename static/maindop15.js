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
                
                // Ячейка ID
                let tdId = document.createElement('td');
                tdId.innerHTML = `<span style="color: #666; font-size: 12px;">#${films[i].id}</span>`;
                
                // Ячейка для русского названия
                let tdTitleRus = document.createElement('td');
                tdTitleRus.innerHTML = `<span class="russian-title">${films[i].title_ru}</span>`;
                
                // Ячейка для оригинального названия
                let tdTitle = document.createElement('td');
                if (films[i].title && films[i].title !== films[i].title_ru) {
                    tdTitle.innerHTML = `<div class="original-title">(${films[i].title})</div>`;
                } else {
                    tdTitle.innerHTML = '<div class="original-title" style="color: #aaa;">(без оригинального названия)</div>';
                }
                
                let tdYear = document.createElement('td');
                tdYear.innerHTML = `<strong>${films[i].year}</strong>`;
                
                // Ячейка для длины описания
                let tdDescLength = document.createElement('td');
                let descLength = films[i].description.length;
                let descColor = descLength > 1800 ? '#e74c3c' : descLength > 1500 ? '#f39c12' : '#27ae60';
                tdDescLength.innerHTML = `<span style="font-size: 11px; color: ${descColor};">
                    ${descLength}/2000
                </span>`;
                
                // Ячейка даты создания
                let tdDate = document.createElement('td');
                if (films[i].created_at) {
                    const date = new Date(films[i].created_at);
                    tdDate.innerHTML = `<span style="font-size: 11px; color: #7f8c8d;">
                        ${date.toLocaleDateString()}
                    </span>`;
                }
                
                let tdActions = document.createElement('td');
                tdActions.style.minWidth = '180px';
                
                // Кнопка редактирования
                let editButton = document.createElement('button');
                editButton.className = 'edit-btn';
                editButton.innerHTML = '✏️';
                editButton.title = 'Редактировать';
                editButton.onclick = function() {
                    editFilm(films[i].id);
                };
                
                // Кнопка удаления
                let delButton = document.createElement('button');
                delButton.className = 'delete-btn';
                delButton.innerHTML = '🗑️';
                delButton.title = 'Удалить';
                delButton.onclick = function() {
                    deleteFilm(films[i].id, films[i].title_ru);
                };
                
                tdActions.append(editButton);
                tdActions.append(delButton);
                
                tr.append(tdId);
                tr.append(tdTitleRus);
                tr.append(tdTitle);
                tr.append(tdYear);
                tr.append(tdDescLength);
                tr.append(tdDate);
                tr.append(tdActions);
                
                tbody.append(tr);
            }
            
            // Загружаем статистику
            loadStats();
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке фильмов:', error);
            showNotification('Ошибка при загрузке фильмов', 'error');
        });
}

// Загрузка статистики
function loadStats() {
    fetch('/lab7/rest-api/stats/')
        .then(response => response.json())
        .then(stats => {
            const statsElement = document.getElementById('stats');
            if (statsElement) {
                statsElement.innerHTML = `
                    <strong>Статистика:</strong> 
                    ${stats.total_films} фильмов | 
                    Годы: ${stats.min_year || '—'}–${stats.max_year || '—'} | 
                    Средний год: ${stats.avg_year || '—'}
                `;
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке статистики:', error);
        });
}

// Отправка фильма (обновлённая функция с обработкой всех ошибок)
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
    
    // Показываем счётчик символов для описания
    updateCharCounter();
    
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
            clearErrors();
            
            // Обработка всех возможных ошибок
            const errorFields = {
                'title_ru': 'title_ru',
                'title': 'title',
                'year': 'year',
                'description': 'description'
            };
            
            for (const [field, elementId] of Object.entries(errorFields)) {
                if (result.errors[field]) {
                    const errorElement = document.getElementById(elementId + '_error');
                    const inputElement = document.getElementById(elementId);
                    
                    if (errorElement) {
                        errorElement.textContent = result.errors[field];
                    }
                    
                    if (inputElement) {
                        inputElement.classList.add('error-field');
                        
                        // Особые обработки
                        if (field === 'description' && result.errors[field].includes('сейчас:')) {
                            const match = result.errors[field].match(/сейчас:\s*(\d+)/);
                            if (match) {
                                const currentLength = parseInt(match[1]);
                                document.getElementById('charCount').textContent = 
                                    `${currentLength}/2000 (превышено на ${currentLength - 2000})`;
                                document.getElementById('charCount').style.color = '#e74c3c';
                            }
                        }
                    }
                }
            }
        }
    })
    .catch(function(error) {
        showNotification('Ошибка при сохранении фильма', 'error');
        console.error('Ошибка:', error);
    });
}

// Функция для обновления счётчика символов
function updateCharCounter() {
    const description = document.getElementById('description').value;
    const charCount = description.length;
    const charCountElement = document.getElementById('charCount');
    
    if (!charCountElement) {
        // Создаём элемент если его нет
        const label = document.querySelector('label[for="description"]');
        if (label) {
            const counter = document.createElement('div');
            counter.id = 'charCount';
            counter.className = 'char-counter';
            label.appendChild(counter);
        }
    }
    
    const counterElement = document.getElementById('charCount');
    if (counterElement) {
        counterElement.textContent = `${charCount}/2000`;
        
        if (charCount > 2000) {
            counterElement.style.color = '#e74c3c';
            counterElement.innerHTML = `${charCount}/2000 <span style="color: #e74c3c">(превышено на ${charCount - 2000})</span>`;
        } else if (charCount > 1800) {
            counterElement.style.color = '#f39c12';
        } else if (charCount > 0) {
            counterElement.style.color = '#27ae60';
        } else {
            counterElement.style.color = '#95a5a6';
        }
    }
}

// Обработчик ввода для описания
document.addEventListener('DOMContentLoaded', function() {
    const descriptionInput = document.getElementById('description');
    if (descriptionInput) {
        descriptionInput.addEventListener('input', updateCharCounter);
    }
});


function fillFilmList(){
    fetch('/lab7/rest-api/films/')
    .then(function(data){
        return data.json();
    })
    .then(function(films){
        let tbody = document.getElementById('film-list');
        tbody.innerHTML='';
        for(let i = 0; i<films.length; i++){
            let tr = document.createElement('tr');

            let tdTitle = document.createElement ('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitle.innerText=film[i].title;
            tdTitleRus.innerText = film [i].title_ru;
            tdYear.innerText = film[i].year;

            let editButton = document.createElement('button');
            editButton.innerText='редактировать';

            let delButton=document.createElement('button');
            delButton.innerText= 'удалить'

            tr.append(tdTitle);
            tr.append(tdTitleRus);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
}
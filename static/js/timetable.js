import { BASE_PATH } from './config.js';
import { getCookie, header_timetable } from './usefulFunctions.js'


window.addEventListener('load', (e) =>{
    let current_weekday = new Date().getDay();

    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/week?data=' + encodeURIComponent(current_weekday);
    xhr.open('GET', url);

    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Authorization", getCookie('token'));
    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            let response = JSON.parse(xhr.response)

            updateSchedule(response);
        }
    }
});


weekdayForm.addEventListener('submit', (e) => {
    e.preventDefault();

    let weekday = document.getElementById('selection').value;

    let weekday_to_num = {
        'Понедельник': 0,
        'Вторник': 1,
        'Среда': 2,
        'Четверг': 3,
        'Пятница': 4,
        'Суббота': 5,
        'Воскресенье': 6,
    }

    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/week?data=' + encodeURIComponent(weekday_to_num[weekday]);
    xhr.open('GET', url);

    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Authorization", getCookie('token'));
    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            let response = JSON.parse(xhr.response)

            updateSchedule(response);
        }
    }
});


function updateSchedule(new_schedule){
    let table = document.querySelector('.tb_table');
    table.innerHTML = '';

    add_line(table, 'Время', 'Предмет', 'Кабинет')

    for(let i = 0; i < new_schedule['name'].length; ++i){
        add_line(table, new_schedule.time[i], new_schedule.name[i], new_schedule.location[i]);
    }

    for(let i = new_schedule['name'].length; i < 8; ++i){
        add_line(table);
    }
}


function add_line(parent, time='', name='Нет урока', location=''){
    let line = document.createElement('tr');

    let time_tr = document.createElement('td');
    time_tr.innerHTML = time;
    let name_tr = document.createElement('td');
    name_tr.innerHTML = name;
    let location_tr = document.createElement('td');
    location_tr.innerHTML = location;
    
    line.appendChild(time_tr);
    line.appendChild(name_tr);
    line.appendChild(location_tr);

    parent.appendChild(line);
}
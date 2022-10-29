import { BASE_PATH } from './config.js';

submitButton.addEventListener("click", (e) => {
e.preventDefault()

let name = nameField.value

    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/get-weekly-timetable-for-student?name=' + encodeURIComponent(name);

    xhr.open('GET', url);

    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            let response = JSON.parse(xhr.response);
            let table = document.getElementById('timetablesTable');

            Object.keys(response).forEach(element => {
//                console.log(element, response[element])
            if (element.length > 0){
            updateSchedule(response[element], element)
            }
            });
        }
    }
})

function updateSchedule(new_schedule, day_of_the_week){
    let table = document.querySelector('#timetablesTable');
    table.innerHTML = '';

    add_line(table, 'Время', 'Предмет', 'Кабинет', 'День недели')

    new_schedule.forEach(element => {
        add_line(table, element.start_time, element.subject_name, element.room_id, day_of_the_week)
    })

}


function add_line(parent, time='', name='Нет урока', location='', day_of_the_week=''){
    let line = document.createElement('tr');

    let time_tr = document.createElement('td');
    time_tr.innerHTML = time;
    let name_tr = document.createElement('td');
    name_tr.innerHTML = name;
    let location_tr = document.createElement('td');
    location_tr.innerHTML = location;
    let day_of_the_week_tr = document.createElement('td');
    day_of_the_week_tr.innerHTML = day_of_the_week;

    line.appendChild(time_tr);
    line.appendChild(name_tr);
    line.appendChild(location_tr);
    line.appendChild(day_of_the_week_tr);

    parent.appendChild(line);
}

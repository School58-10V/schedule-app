import { BASE_PATH } from './config.js';

function request(){
    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/get-weekly-timetable-for-student/' + name;

    xhr.open('GET', url);

    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            let response = JSON.parse(xhr.response);
            let table = document.getElementById('timetablesTable');

            response.forEach(element => {
                let row = table.insertRow(1);
                let id = row.insertCell(0);
                let day_of_the_week = row.insertCell(1);
                let group_id = row.insertCell(2);
                let subject_id = row.insertCell(3);
                let room_id = row.insertCell(4);
                let start_time = row.insertCell(5);
                let end_time = row.insertCell(6);
                let timetable_id = row.insertCell(7);

                id.innerHTML = element['object_id'];
                day_of_the_week.innerHTML = element['day_of_the_week'];
                group_id.innerHTML = element['group_id'];
                subject_id.innerHTML = element['subject_id'];
                room_id.innerHTML = element['room_id'];
                start_time.innerHTML = element['start_time'];
                end_time.innerHTML = element['end_time'];
                timetable_id.innerHTML = element['timetable_id'];
            });
        }
    }
}

if(name._length == 1) {request()}
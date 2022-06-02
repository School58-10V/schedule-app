import { BASE_PATH } from './config.js';

function request(){
    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/lesson';

    xhr.open('GET', url);

    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            let response = JSON.parse(xhr.response);
            let table = document.getElementById('lessonsTable');

            response.forEach(element => {
                let row = table.insertRow(1);

                let id = row.insertCell(0);
                let date = row.insertCell(1);
                let class_id = row.insertCell(2);
                let name = row.insertCell(3);
                let subject_id = row.insertCell(4);
                let teacher_id = row.insertCell(5);

                id.innerHTML = element['object_id'];
                date.innerHTML = element['date'];
                class_id.innerHTML = element['group_id'];
                name.innerHTML = element['notes'];
                subject_id.innerHTML = element['subject_id'];
                teacher_id.innerHTML = element['teacher_id'];
            });
        }
    }
}

request();
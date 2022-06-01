import { BASE_PATH } from './config.js';

function request(){
    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/teachers';

    xhr.open('GET', url);

    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            let response = JSON.parse(xhr.response);
            let table = document.getElementById('teachersTable');

            print(table.children);

            response.forEach(element => {
                let row = table.insertRow(1);

                let id = row.insertCell(0);
                let fullname = row.insertCell(1);
                let bio = row.insertCell(2);
                let constacts = row.insertCell(3);
                let lessons = row.insertCell(4);
                let subjects = row.insertCell(5);
                let offices = row.insertCell(5);

                id.innerHTML = element['object_id'];
                fullname.innerHTML = element['fio'];
                bio.innerHTML = element['bio'];
                constacts.innerHTML = element['contacts'];
                lessons.innerHTML = element['lesson_row_id'];
                subjects.innerHTML = element['subject_id'];
                offices.innerHTML = element['office_id'];
            });
        }
    }
}

request();
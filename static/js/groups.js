import { BASE_PATH } from './config.js';

function request(){
    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/group';

    xhr.open('GET', url);

    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            let response = JSON.parse(xhr.response);
            let table = document.getElementById('groupsTable');

            response.forEach(element => {
                let row = table.insertRow(2);

                let id = row.insertCell(0);
                let grade = row.insertCell(1);
                let class_letter = row.insertCell(2);
                let profile_name = row.insertCell(3);
                let students = row.insertCell(4);
                let teacher = row.insertCell(5);

                id.innerHTML = element['object_id'];
                grade.innerHTML = element['grade'];
                class_letter.innerHTML = element['class_letter'];
                profile_name.innerHTML = element['profile_name'];
                students.innerHTML = element['students'];
                teacher.innerHTML = element['teacher_id'];
            });
        }
    }
}

request();
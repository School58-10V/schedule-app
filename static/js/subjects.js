import { BASE_PATH } from './config.js';

function request(){
    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/subjects';

    xhr.open('GET', url);

    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            let response = JSON.parse(xhr.response);
            let table = document.getElementById('subjectsTable');

            response.forEach(element => {
                let row = table.insertRow(1);

                let id = row.insertCell(0);
                let name = row.insertCell(1);
                let teachers = row.insertCell(2)

                id.innerHTML = element['object_id'];
                name.innerHTML = element['subject_name'];
                teachers.innerHTML = element['teachers'];
            });
        }
    }
}

request();
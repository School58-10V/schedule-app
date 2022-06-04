import { BASE_PATH } from './config.js';

function request(){
    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/students';

    xhr.open('GET', url);

    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            let response = JSON.parse(xhr.response);
            let table = document.getElementById('studentsTable');

            response.forEach(element => {
                let row = table.insertRow(1);

                let id = row.insertCell(0);
                let fullname = row.insertCell(1);
                let birthdate = row.insertCell(2);
                let constacts = row.insertCell(3);
                let bio = row.insertCell(4);
                let groupsId = row.insertCell(5);

                id.innerHTML = element['object_id'];
                fullname.innerHTML = element['full_name'];
                birthdate.innerHTML = element['date_of_birth'];
                constacts.innerHTML = element['contacts'];
                bio.innerHTML = element['bio'];
                groupsId.innerHTML = element['groups'];
            });
        }
    }
}

request();
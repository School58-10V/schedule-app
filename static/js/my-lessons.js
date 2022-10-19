import {BASE_PATH} from './config.js';
import {getCookie} from "./usefulFunctions.js";


function request() {
    let url = BASE_PATH + '/week';
    fetch(url, {
        method: 'GET',
        headers: {
            "Authorization": getCookie('token')
        }
    }).then(async (resp) => {
        console.log(resp.status)
        if (resp.status === 401) {
            alert('Вы не можете пользоваться этой страницей т.к. вы не авторизованы или ваш токен истек')
            return
        }
        if ((await resp.text()).length === 0) {
            // no lessons yay
            // let table = document.getElementById('my-lessonsTable');
            // table.replaceWith('уроков нет! ура!');
        } else {

        }
    })

    // xhr.onload = () => {
    //     if (xhr.status == 200) {
    //         let response = JSON.parse(xhr.response);
    //         let table = document.getElementById('subjectsTable');
    //
    //         response.forEach(element => {
    //             let row = table.insertRow(1);
    //
    //             let id = row.insertCell(0);
    //             let name = row.insertCell(1);
    //             let teachers = row.insertCell(2)
    //
    //             id.innerHTML = element['object_id'];
    //             name.innerHTML = element['subject_name'];
    //             teachers.innerHTML = element['teachers'];
    //         });
    //     }
    // }
}

request();
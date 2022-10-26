import { BASE_PATH } from './config.js'
import { setCookie } from './usefulFunctions.js'

sendButton.addEventListener('click', (e)=>{
    e.preventDefault();
    alert('123');
    let request = new XMLHttpRequest();
    let url = BASE_PATH + '/groups';
    request.open('POST', url);
//    let lesson_rows = lesson_row_id.value;
//

    let id = document.getElementById("id").value

    let data = JSON.stringify({
        "id": document.getElementById("id").value,
        "grade": document.getElementById("grade").value,
        "profile_name": document.getElementById("profile_name").value,
        "students": document.getElementById("students").value,
        "teacher": document.getElementById("teacher").value
    });
    request.withCredentials = true;
    request.setRequestHeader("Content-Type", "application/json");

    request.send(data);
    id.value = '';
    grade.value = '';
    profile_name.value = '';
    students.value = '';
    teacher.value = '';
    request.onload = () => {
        if(request.status === 200){
            let response = JSON.parse(request.response);

            let token = response['token'];

            let time = {
                'seconds': 0, 'minutes': 0, 'hours': 0, 'days': 14
            };

            setCookie('token', token, time);

            window.location.pathname = '/';
        }
        else if (request.status === 401){
            loginField.style.borderColor = 'red';
            passwordField.style.borderColor = 'red';
            loginField.placeholder = 'Неверные данные';
        }
    };
})
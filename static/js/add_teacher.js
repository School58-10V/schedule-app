import { BASE_PATH } from './config.js'
import { setCookie } from './usefulFunctions.js'


sendButton.addEventListener('click', (e)=>{
    e.preventDefault();
    alert('123');
    let request = new XMLHttpRequest();
    let url = BASE_PATH + '/teachers';
    request.open('POST', url);
//    let lesson_rows = lesson_row_id.value;
//
    let data = JSON.stringify({
        "fio": fio.value,
        "bio": bio.value,
        "contacts": contacts.value,
        "office_id": office_id.value,
    });
    request.withCredentials = true;
    request.setRequestHeader("Content-Type", "application/json");

    request.send(data);
    fio.value = '';
    bio.value = '';
    contacts.value = '';
    office_id.value = '';
    request.onload = () => {
        if(request.status == 200){
            let response = JSON.parse(request.response);

            let token = response['token'];

            let time = {
                'seconds': 0, 'minutes': 0, 'hours': 0, 'days': 14
            };

            setCookie('token', token, time);

            window.location.pathname = '/';
        }
        else if (request.status == 401){
            loginField.style.borderColor = 'red';
            passwordField.style.borderColor = 'red';
            loginField.placeholder = 'Неверные данные';
        }
    };
})
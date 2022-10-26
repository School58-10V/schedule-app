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
        "subject_name": subject_name.value,
        "teachers": bio.value
    });
    request.withCredentials = true;
    request.setRequestHeader("Content-Type", "application/json");

    request.send(data);
    subject_name.value = '';
    teachers.value = '';
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
            subject_name.style.borderColor = 'red';
            teachers.style.borderColor = 'red';
            subject_name.placeholder = 'Неверные данные';
        }
    };
})
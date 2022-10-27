import { BASE_PATH } from './config.js';
import { getCookie } from './usefulFunctions.js'

sendButton.addEventListener('click', (e) => {
    e.preventDefault();

    // тут надо будет изменить, чтобы получалось не ID со страницы, а получались названия
    let data = {
        "teacher_id": document.getElementById('teacher_id').value,
        "class_letter": document.getElementById('class_letter').value,
        "grade": document.getElementById('grade').value,
        "profile_name": document.getElementById('profile_name').value,
    };

    data['teacher_id'] = parseInt(data['teacher_id']);
    data['grade'] = parseInt(data['grade']);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', BASE_PATH + '/group');

    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Authorization", getCookie('token'));
    xhr.send( JSON.stringify(data) );
})
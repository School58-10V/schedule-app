import { BASE_PATH } from './config.js';
import { getCookie } from './usefulFunctions.js'

sendButton.addEventListener('click', (e) => {
    e.preventDefault();

    // тут надо будет изменить, чтобы получалось не ID со страницы, а получались названия
    let data = {
        "fio": document.getElementById('fio').value,
        "bio": document.getElementById('bio').value,
        "contacts": document.getElementById('contacts').value,
        "office_id": document.getElementById('class_number').value,
        "subject_id": document.getElementById('subject').value,
        "lesson_row_id": document.getElementById('groups').value.split(' '),
    };
    
    data['subject_id'] = parseInt(data['subject_id']);
    data['office_id'] = parseInt(data['office_id']);
    data['lesson_row_id'] = data['lesson_row_id'].map(x => parseInt(x));

    let xhr = new XMLHttpRequest();
    xhr.open('POST', BASE_PATH + '/teachers');

    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Authorization", getCookie('token'));
    xhr.send( JSON.stringify(data) );
})
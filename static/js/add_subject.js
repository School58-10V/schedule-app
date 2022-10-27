import { BASE_PATH } from './config.js';
import { getCookie } from './usefulFunctions.js'

sendButton.addEventListener('click', (e) => {
    e.preventDefault();

    // тут надо будет изменить, чтобы получалось не ID со страницы, а получались названия
    let data = {
        "subject_name": document.getElementById('subject_name').value,
        "teachers": document.getElementById('teachers').value.split(' '),
    };
    
    data['teachers'] = data['teachers'].map(x => parseInt(x));

    let xhr = new XMLHttpRequest();
    xhr.open('POST', BASE_PATH + '/subjects');

    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Authorization", getCookie('token'));
    xhr.send( JSON.stringify(data) );
})
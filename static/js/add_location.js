import { BASE_PATH } from './config.js';
import { getCookie } from './usefulFunctions.js'

sendButton.addEventListener('click', (e) => {
    e.preventDefault();

    // тут надо будет изменить, чтобы получалось не ID со страницы, а получались названия
    let data = {
        "num_of_class": document.getElementById('num_of_class').value,
        "profile": document.getElementById('profile').value,
        "equipment": document.getElementById('equipment').value,
        "link": document.getElementById('link').value,
        "location_type": document.getElementById('location_type').value,
        //   "location_desc": document.getElementById('location_desc').value, # я так и не поняла, что это и нужно ли нам это
    };

    data['num_of_class'] = parseInt(data['num_of_class']);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', BASE_PATH + '/location');

    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Authorization", getCookie('token'));
    xhr.send( JSON.stringify(data) );
})
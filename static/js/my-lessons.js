import {BASE_PATH} from './config.js';
import {getCookie, generateTablesFromJSON} from "./usefulFunctions.js";



function request() {
    let url = BASE_PATH + '/week';
    if (getCookie('token') === undefined) {
            alert('Вы не можете пользоваться этой страницей т.к. вы не авторизованы или ваш токен истек');
    }
    let options = {
        method: 'GET',
        headers: {
            "Authorization": getCookie('token')
        }
    }

    fetch(url, options).then(async (resp) => {
        if (resp.status === 401) {
            alert('Вы не можете пользоваться этой страницей т.к. вы не авторизованы или ваш токен истек');
            return;
        }
        let json = await resp.json();
        let example_table = document.getElementById('my-lessonsTable-weekday-x');
        if (json.length === 0) {
            example_table.replaceWith('На этой неделе у тебя уроков нет. ура!');
        } else {
            generateTablesFromJSON(json)

        }
    })
}

request();
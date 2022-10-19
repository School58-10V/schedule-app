import {BASE_PATH} from './config.js'
import {setCookie} from './usefulFunctions.js'
// import Cookie from '../../node_modules/js-cookie/dist/js.cookie.mjs'

sendButton.addEventListener('click', (e) => {
    e.preventDefault();

    let url = BASE_PATH + '/login';
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({'login': loginField.value, 'password': passwordField.value}),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(async (resp) => {
        if (resp.status === 200) {
            let token = (await resp.json()).token;

            let time = {
                'seconds': 0, 'minutes': 0, 'hours': 0, 'days': 14
            };

            setCookie('token', token, time);

            window.location.pathname = '/';
        } else if (resp.status === 401) {
            loginField.style.borderColor = 'red';
            passwordField.style.borderColor = 'red';
            loginField.placeholder = 'Неверные данные';
        }
    })

    // request.open('POST', url);

    // let data = JSON.stringify({
    //     "login": loginField.value,
    //     "password": passwordField.value
    // });

    // request.withCredentials = true;
    // request.setRequestHeader("Content-Type", "application/json");

    // request.send(data);

    // loginField.value = '';
    // passwordField.value = '';

    // request.onload = () => {

    // };
})
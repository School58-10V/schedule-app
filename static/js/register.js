import { BASE_PATH } from "./config.js";
import { setCookie } from "./usefulFunctions";


registerButton.addEventListener('click', (e) => {
    e.preventDefault();

    let request = new XMLHttpRequest();
    let url = BASE_PATH + '/register';
    request.open('POST', url);

    let data = JSON.stringify({
        "login": loginField.value,
        "fullname": fullnameField.value,
        "password": passwordField.value
    });

    request.withCredentials = true;
    request.setRequestHeader("Content-Type", "application/json");
    
    request.send(data);

    loginField.value = '';
    fullnameField.value = '';
    passwordField.value = '';

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
    };
});
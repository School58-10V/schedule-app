import { BASE_PATH } from './config.js'
import Cookies from 'js-cookie'


sendButton.addEventListener('click', (e)=>{
    e.preventDefault();

    let request = new XMLHttpRequest();
    let url = BASE_PATH + '/login';
    request.open('POST', url);
    console.log(url);

    let data = JSON.stringify({
        "login": loginField.value,
        "password": passwordField.value
    });

    request.withCredentials = true;
    request.setRequestHeader("Content-Type", "application/json");
    
    request.send(data);

    loginField.value = '';
    passwordField.value = '';

    request.onload = () => {
        if(request.status == 200){
            let response = request.response;

            let token = response['token'];
            console.log(token);

            Cookies.set('token', token, {expires: 14});
        }
    };
})
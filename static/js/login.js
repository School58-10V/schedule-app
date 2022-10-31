const BASE_PATH = '/api/v1'
function setCookie(name, value, time){
    let duration = time['seconds'] + time['minutes'] * 60 +
                    time['hours'] * 3600 + time['days'] * 86400;

    let data = `${name}=${value}; max-age=${duration}; path=/`;
    document.cookie = data;
}


sendButton.addEventListener('click', (e)=>{
    e.preventDefault();

    let request = new XMLHttpRequest();
    let url = BASE_PATH + '/login';
    request.open('POST', url);

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
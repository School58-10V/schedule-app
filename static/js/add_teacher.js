const BASE_PATH = '/api/v1'
function setCookie(name, value, time){
    let duration = time['seconds'] + time['minutes'] * 60 +
                    time['hours'] * 3600 + time['days'] * 86400;

    let data = `${name}=${value}; max-age=${duration}; path=/`;
    document.cookie = data;
}
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}


sendButton.addEventListener('click', (e)=>{
    e.preventDefault();
    alert('123');
    let request = new XMLHttpRequest();
    let url = BASE_PATH + '/teachers';
    request.open('POST', url);
//    let lesson_rows = lesson_row_id.value;
//
    let data = JSON.stringify({
        "fio": fio.value,
        "bio": bio.value,
        "contacts": contacts.value,
        "office_id": office_id.value,
    });
    request.withCredentials = true;
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Authorization",getCookie("token"));
    request.send(data);
    fio.value = '';
    bio.value = '';
    contacts.value = '';
    office_id.value = '';
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
            fio.style.borderColor = 'red';
            bio.style.borderColor = 'red';
            fio.placeholder = 'Неверные данные';
        }
    };
})
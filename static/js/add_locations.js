import { BASE_PATH } from './config.js'
import { setCookie } from './usefulFunctions.js'


let sendButton = document.getElementById("sendButton");
sendButton.addEventListener('click', (e)=>{
    e.preventDefault();
    alert('123');
    let request = new XMLHttpRequest();
    let url = BASE_PATH + '/locations';
    request.open('POST', url);
//    let lesson_rows = lesson_row_id.value;
//
    let data = JSON.stringify({
        "location_type": document.getElementById("location_type").value,
        "location_desc": location_desc.value,
        "profile": profile.value,
        "num_of_class": num_of_class.value,
        "equipment": equipment.value,
        "link": link.value,
        "comment": comment.value
    });
    request.withCredentials = true;
    request.setRequestHeader("Content-Type", "application/json");

    request.send(data);
    location_type.value = '';
    location_desc.value = '';
    profile.value = '';
    num_of_class.value = '';
    equipment.value = '';
    link.value = '';
    comment.value = '';
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
            profile.style.borderColor = 'red';
            equipment.style.borderColor = 'red';
            profile.placeholder = 'Неверные данные';
        }
    };
})
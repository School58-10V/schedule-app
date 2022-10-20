import { BASE_PATH } from './config.js';
import { getCookie } from './usefulFunctions.js'


getSchedule.addEventListener('click', (e) => {
    e.preventDefault();

    let weekday = document.getElementById('selection').value;
    
    let data = JSON.stringify({
        "weekday": weekday
    });

    let xhr = new XMLHttpRequest();
    let url = '/timetable?data=' + encodeURIComponent(data);
    xhr.open('POST', url);
    
    // console.log(getCookie('token'))

    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Authorization", getCookie('token'));
    xhr.send();

    xhr.onload = ()=>{
        if(xhr.status == 200){
            // let response = JSON.parse(xhr.response);
            // let elem = document.getElementById('timetable');
            console.log(xhr.response);
            // elem.innerHTML = xhr.response;
        }
    }
});
import { BASE_PATH } from './config.js';
const TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJsb2dpbiI6Im1hdm92ayIsInVzZXJfaXAiOiIxMjcuMC4wLjEiLCJ1c2VyX2FnZW50IjoiUG9zdG1hblJ1bnRpbWUvNy4yOS4yIiwiZXhwIjoxNjY3MjM4MTQ4fQ.lF4b7PKgjmxacOJ5DJ4g-IsEX4dFw4mY4BNurgVvkgjmk0tAoXSHOj34PmbUbS_qsWM0nzGvrrXw40GcVOHQDyDyrUbNi1Gm4kR-NbAuiN5mXBoYqdGZlfXz__Xdg1HbSAfMHheAyc0BkoOrfs9IO8OzogQr9BYLUcwW3LG-2Tgcj2VZrdhS8LN9Xm5aYx6L62nY_ORA9saJQS5AsELkgLGdOR3gydtPZZDCUnkMT_tCFux0lv2nWMyxexyPnRkJqtxVI-TtZxrAPluVNLec1jaraBOVA-rh3d4yjUC45dCATrSeBNde_8OxVwLJRPmUVEi5w9jOilW6fmZTTuNPjw'


getSchedule.addEventListener('click', (e) => {
    e.preventDefault();

    let weekday = weekday.value;

    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/timetable';
    xhr.open('GET', url);

    let data = JSON.stringify({
        "full_name": studentName
    });

    // Хромов Михаил Романович
    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    console.log(data);
    xhr.send(data);
    console.log(xhr);

    xhr.onload = ()=>{
        if(xhr.status == 200){
            // let response = JSON.parse(xhr.response);
            let elem = document.getElementById('timetable');
            console.log(xhr.response);
            elem.innerHTML(xhr.response);
        }
    }
});
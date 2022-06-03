import { BASE_PATH } from './config.js';


submitButton.addEventListener('click', (e) => {
    e.preventDefault();

    let studentName = nameField.value;
    nameField.value = '';
    
    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + '/week';
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
import {BASE_PATH} from "./config.js";
import {generateTablesFromJSON, getCookie} from "./usefulFunctions.js";

let LESSONS_JSON;
const WEEKDAY_OBJECT = document.getElementById('select-weekday');
const NO_LESSON_OBJECT = document.getElementById('no-lessonrow-today');


function generateTablesForDayFromJSON(json, weekday) {
    let today_lessons = [];
    for (let x in json) {
        console.log(json[x])
        if (json[x].weekday === weekday) {
            today_lessons.push(json[x]);
        }
    }
    console.log(today_lessons)
    console.log(weekday)

    let example_table = document.getElementById('my-lessonsTable-weekday-x');
    if (today_lessons.length === 0) {
        NO_LESSON_OBJECT.hidden = false;
    } else {
        NO_LESSON_OBJECT.hidden = true;
        generateTablesFromJSON(today_lessons)
    }
}


function request() {
    let url = BASE_PATH + '/week';
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
        LESSONS_JSON = await resp.json();
        // сдвиг на -1 тк в жс воскресенье=0, пн=1, тд (а в бд вс=6, пн=1)
        let today_weekday = (new Date().getDay() - 1) % 7;
        generateTablesForDayFromJSON(LESSONS_JSON, today_weekday)
    })
}

request();


function redoTables() {
    // deleting old tables
    for (let i = 0; i < 7; i++) {
        try {
            document.getElementById('my-lessonsTable-weekday-' + String(i)).remove();
        } catch (e) {

        }
    }
    generateTablesForDayFromJSON(LESSONS_JSON, parseInt(WEEKDAY_OBJECT.value));
}

WEEKDAY_OBJECT.onchange = redoTables


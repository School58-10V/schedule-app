export function requestPOST(url, data) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', url);

    data = JSON.stringify(data);

    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send(data);

    xhr.onload = () => {
        if (xhr.status == 200) {
            return xhr.response;
        } else {
            throw xhr.status
        }
    };
}

export function setCookie(name, value, time) {
    let duration = time['seconds'] + time['minutes'] * 60 +
        time['hours'] * 3600 + time['days'] * 86400;

    let data = `${name}=${value}; max-age=${duration}; path=/`;
    document.cookie = data;
}

export function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

export function deleteCookie(name) {
    let time = {
        'seconds': -1, 'minutes': 0, 'hours': 0, 'days': 0
    };
    setCookie(name, '', time);
}

export function generateTablesFromJSON(json) {
    let example_table = document.getElementById('my-lessonsTable-weekday-x');

    let weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', "Пятница", "Суббота", "Воскресенье"];
    let weekday_tables = {};
    let last_element = null;
    console.log(json)
    json.forEach((el) => {
        if (weekday_tables[el.weekday] === undefined) {
            let obj = example_table.cloneNode(true);
            obj.children[0].innerHTML = weekdays[el.weekday];
            obj.id = 'my-lessonsTable-weekday-' + String(el.weekday);
            obj.hidden = false;
            weekday_tables[el.weekday] = obj;

            if (last_element === null)
                example_table.after(weekday_tables[el.weekday]);
            else
                last_element.after(weekday_tables[el.weekday]);
            last_element = weekday_tables[el.weekday];
        }
        // add the lesson
        let table = weekday_tables[el.weekday].children[1];
        let row = table.insertRow(1);
        let time_start = row.insertCell(0);
        let time_end = row.insertCell(1);
        let subject = row.insertCell(2);
        let location_number = row.insertCell(3);
        let teacher_full_name_list = row.insertCell(4);
        console.log(el)
        time_start.innerHTML = el.start_time;
        time_end.innerHTML = el.end_time;
        subject.innerHTML = el.subject;
        location_number.innerHTML = el.location_number;
        teacher_full_name_list.innerHTML = el.teacher_full_name_list;
    })
}


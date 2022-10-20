export function requestPOST(url, data){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', url);

    data = JSON.stringify(data);

    xhr.withCredentials = true;
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.send(data);

    xhr.onload = () => {
        if(xhr.status == 200){
            return xhr.response;
        } 
        else{
            throw xhr.status
        }
    };
}

export function setCookie(name, value, time){
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

export function deleteCookie(name){
    let time = {
        'seconds': -1, 'minutes': 0, 'hours': 0, 'days': 0
    };
    setCookie(name, '', time);
}


export let header_timetable = `<tr>
<td style="width: 28%; height: 12%">Дата</td>
<td style="width: 57%">Предмет</td>
<td>Кабинет</td>
</tr>`;





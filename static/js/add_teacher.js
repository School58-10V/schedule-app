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
    let data_subject_id = subject_id.value.split(' ');
    let subject_id_lst = [];
    for (let i=0; i < data_subject_id.length; i+= 1){
    let x = parseInt(data_subject_id[i], 10);
    subject_id_lst.push(x);}
    let data_lesson_row_id = lesson_row_id.value.split(' ');
    let lesson_row_id_lst = [];

    for (let i=0; i < data_lesson_row_id.length; i+= 1){

    alert('123');
    let x = parseInt(data_lesson_row_id[i], 10);
    lesson_row_id_lst.push(x);}
    alert('-----');
    let office_id_int = parseInt(office_id.value);
    let data = JSON.stringify({
        "fio": fio.value,
        "bio": bio.value,
        "contacts": contacts.value,
        "office_id": office_id_int,
        'lesson_row_id': lesson_row_id_lst,
        'subject_id': subject_id_lst,
    });
    request.withCredentials = true;
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.setRequestHeader("Authorization",getCookie("token"));
    request.send(data);
    fio.value = '';
    bio.value = '';
    contacts.value = '';
    office_id.value = '';
    alert('======');
    request.onload = () => {
         if (request.status === 401){
            fio.style.borderColor = 'red';
            bio.style.borderColor = 'red';
            fio.placeholder = 'Неверные данные';
        }
    };
})
const BASE_PATH = '/api/v1';

let page = 0;

const student_id = 122;

function scrollLeft() {
    return scroll(-1);
}

function scrollRight() {
    return scroll(1);
}

function scroll(amount) {
    if (page + amount < 0) {
        page = 6
    } else if (page + amount > 6) {
        page = 0
    } else {
        page += amount
    }
    getTimeTable(page, student_id);
}

function getTimeTable(day, student_id) {

    const buttons = document.getElementsByClassName("numbutton");
    console.log(buttons);
    for (let element of buttons) {
        console.log(typeof element);
        element.style.backgroundColor = "whitesmoke";
    };

    document.getElementById("day" + (day + 1)).style.backgroundColor = "red";

    let xhr = new XMLHttpRequest();
    let url = BASE_PATH + "/lesson-row/personal?" + "day=" + encodeURIComponent(day) + "&student_id=" + encodeURIComponent(student_id);

    xhr.open("GET", url);
    xhr.send();

    xhr.onload = () => {
        if (xhr.status === 200) {
            let response = JSON.parse(xhr.response);
            let table = document.getElementById("table");

            response.forEach(element => {
                let row = table.insertRow(1);

                let id = row.insertCell(0);
                let subject = row.insertCell(1);
                let start_time = row.insertCell(2);

                id.innerHTML = element["object_id"];
                subject.innerHTML = element["subject_name"];
                start_time.innerHTML = element["start_time"];
            });
        }
    }
}

document.getElementById("left_b").onclick = scrollLeft;
document.getElementById("right_b").onclick = scrollRight;

document.getElementById("day1").addEventListener("click", (event) => {getTimeTable(0, student_id)});
document.getElementById("day2").addEventListener("click", (event) => {getTimeTable(1, student_id)});
document.getElementById("day3").addEventListener("click", (event) => {getTimeTable(2, student_id)});
document.getElementById("day4").addEventListener("click", (event) => {getTimeTable(3, student_id)});
document.getElementById("day5").addEventListener("click", (event) => {getTimeTable(4, student_id)});
document.getElementById("day6").addEventListener("click", (event) => {getTimeTable(5, student_id)});
document.getElementById("day7").addEventListener("click", (event) => {getTimeTable(6, student_id)});

getTimeTable(0, student_id);

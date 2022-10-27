import {BASE_PATH} from './config.js'
import {getCookie} from './usefulFunctions.js'

const createObjectForm = document.getElementById('addObjectForm');
const objectCreatedSuccessParagraph = document.getElementById('objectCreatedSuccessParagraph');

createObjectForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (getCookie("token") === undefined) {
        alert("Ты не можешь создавать что-то, ты не авторизован!");
        return;
    }

    let inputObjectDict = {};
    let list_of_inputs = [];
    let c = 0;
    while (true) {
        if (createObjectForm[c] !== undefined) {
            list_of_inputs.push(createObjectForm[c]);
            c += 1;
        } else {
            break;
        }
    }
    list_of_inputs.forEach((el) => {
        if (el.tagName === "INPUT" && el.value !== "Создать") {
            let val = el.value;
            if (el.dataset.type === 'number') {
                val = parseInt(val);
            } else if (el.dataset.type === 'list') {
                val = val.split(',').map(parseFloat);
                console.log(val)
            }
            inputObjectDict[el.name] = val;
        }
    })
    console.log(inputObjectDict)
    let url = BASE_PATH + '/' + inputObjectDict["object_type"];
    delete inputObjectDict["object_type"];
    let options = {
        method: "POST",
        headers: {
            "Authorization": getCookie("token"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify(inputObjectDict)

    };
    fetch(url, options).then(async (resp) => {
        console.log(await resp.text());
        console.log(resp.status);
        if (resp.status !== 200) {
            alert("some error idk")
            return;
        }
        objectCreatedSuccessParagraph.hidden = false;

    })

})


function requestPOST(url, data){
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

export default requestPOST;
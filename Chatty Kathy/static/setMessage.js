function setMessage(message){
    var httpRequest = new XMLHttpRequest();

    if(!httpRequest){
        alert('Does your browser support AJAX?');
        return false;
    }
    httpRequest.open('POST', '/setMessage');
    httpRequest.setRequestHeader('Content-Type', 'application/json', 'charset=utf-8');
    let user = "{{session['user_id']}}";

    let info = JSON.stringify(
        {
            msg: message
        }
    );
    httpRequest.send(info);  
}
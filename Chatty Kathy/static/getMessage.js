function getMessage(){
    var httpRequest = new XMLHttpRequest();

    if(!httpRequest){
        alert('Does your browser support AJAX?');
        return false;
    }

    httpRequest.onreadystatechange = function() {
        elementHandler(httpRequest);
    };

    httpRequest.open("GET", "/getMessage");
    httpRequest.send();
    
}

function elementHandler(httpRequest){
    if(httpRequest.readyState === XMLHttpRequest.DONE){
        if(httpRequest.status === 200){
            console.log(httpRequest.responseText);
            if(httpRequest.responseText === 'Please leave this room as soon as you as can! I would like to go home!'){
                window.location.href = '/join_chatroom'
            }
            else{
                const message = JSON.parse(httpRequest.responseText);
                const table = document.getElementById('chatTbl').getElementsByTagName('tbody')[0];
                const time = new Date(Date.now() - 1000);
                const timeString = (time.getMonth() + 1) + "/" + time.getDate() + "/" + time.getFullYear() + " " + time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds();

                for(var i = 0; i < message.length; i++){
                    let row = table.insertRow(table.rows.length);
                    let cell = row.insertCell(0).appendChild(document.createTextNode(message[i][1]));
                    let timeCell = row.insertCell(1).appendChild(document.createTextNode(timeString));
                    let userCell = row.insertCell(2).appendChild(document.createTextNode(message[i][0]));
                }
            }
        }
        else{
            document.getElementById('ajaxError').style.display = 'blocks';
        }
    }
}



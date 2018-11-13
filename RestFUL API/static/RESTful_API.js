/* POST Budget Category */ 
function postCategories(user, limit){
    var xhttp = new XMLHttpRequest();

    if(!xhttp){
        alert('Does your browser support AJAX?');
        return false;
    }

    xhttp.getreadystatechange = function(){
        if(this.status == 201){
            logxhttp(this.responseText, 'Executed POST', this.status);
        }
        else if(this.status == 404){
            logxhttp(this.responseText, 'Error using POST in request', this.status);
        }
    }

    xhttp.open("POST", "/cats");
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=utf-8');

    const cat = JSON.stringify({
        type: user,
        limit: limit
    });

    xhttp.send(cat);

}

/* GET Specific Budget Category */
function getCategories(catID){
    var xhttp = new XMLHttpRequest();

    if(!xhttp){
        alert('Does your browser support AJAX?');
        return false;
    }

    xhttp.getreadystatechange = function(){
        if(this.status == 201){
            logxhttp(this.responseText, 'Executed GET', this.status);
        }
        else if(this.status == 404){
            logxhttp(this.responseText, 'Error using GET in request', this.status);
        }
    }

    xhttp.open("GET", "/cats");
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
    xhttp.send();
}

/* GET All Budget Categories */
function getAllCategories() {
    var xhttp = new XMLHttpRequest();

    if(!xhttp){
        alert('Does your browser support AJAX?');
        return false;
    }

    xhttp.getreadystatechange = function(){
        if(this.status == 200){
            logxhttp(this.responseText, 'Executed GET', this.status);
        }
    }

    xhttp.open("GET", "/cats");
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
    xhttp.send();
}

/* PUT Purchase Category */
function putPurchases(spent, object, catID, purchaseDate){
    var xhttp = new XMLHttpRequest();

    if(!xhttp){
        alert('Does your browser support AJAX?');
        return false;
    }

    xhttp.open("PUT", "/purchases");
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=utf-8');

    const purchase = JSON.stringify({
        cat_id: catID,
        object: object,
        date: purchaseDate,
        spent: spent
    });

    xhttp.send(purchase);
}

/* GET Purchase Category */
function getPurchase() {
    var xhttp = new XMLHttpRequest();

    if(!xhttp){
        alert('Does your browser support AJAX?');
        return false;
    }

    xhttp.open("GET", "/purchases");
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
    xhttp.send();
}

/* DELETE Category */
function deleteCatories(catID, name){
    var xhttp = new XMLHttpRequest();

    if(!xhttp){
        alert('Does your browser support AJAX?');
        return false;
    }

    xhttp.getreadystatechange = function(){
        if(this.status == 200){
            logxhttp(this.responseText, 'Executed GET', this.status);
        }
    }

    xhttp.open("DELETE", "/cats/" + catID);
    xhttp.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
    xhttp.send();
}

function logxhttp(response, message, code){
    console.log(code);
    console.log(message);
    console.log(response);
}

function fillContent(response){
    let response = JSON.parse(response);
    var mapText = response.map();
}

window.onload = function(){
    getAllCategories();
    getPurchase();
}

/* Button Event Listeners */
/* Add Budget Button */
document.getElementById('add').addEventListener('click', function(event){
    event.stopImmediatePropagation();
    event.preventDefault();

    let catName = document.getElementById('name');
    let catLimit = document.getElementById('limit');

    postCategories(catName.value, catLimit.value);

    catName.value = '';
    catLimit.value = '';
});

/* Add Purchase Button */
document.getElementById('addPurchase').addEventListener('click', function(event){
    event.stopImmediatePropagation();
    event.preventDefault();

    let purchaseSpent = document.getElementById('amountSpent');
    let purchaseObject = document.getElementById('spentOn');
    let purchDate = document.getElementById('purchaseDate');
    let purchaseCat = sessionStorage.getItem('cat_id');

    putPurchases(purchaseSpent.value, purchaseObject.value, purchaseCat, purchDate.value);

    purchaseSpent.value = '';
    purchaseObject.value = '';
    purchDate.value = '';
    purchaseCat.value = '';
});

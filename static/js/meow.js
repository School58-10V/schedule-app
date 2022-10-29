let d = new Date();
document.getElementById('meow').innerHTML = "<h1>Today's date is " + d + "</h1>"

alert("Meow");

alert("More Meow");

var button = document.createElement("button");
button.innerHTML = "DO MEOW";
var body = document.getElementsByTagName("body")[0];
body.appendChild(button);
button.addEventListener ("click", function() {alert("DID MEOW")});
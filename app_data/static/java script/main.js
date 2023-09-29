


var x = document.getElementById('gmail')
var y = document.getElementById('pass')

function move(){
    x.style.visibility='hidden';
    y.style.left='10%';
}

var z = document.getElementById('show_pass')
function show(x){
    if(x.checked==true)
    {
        z.type="text";
    }
    else
    {
        z.type="password";
    }
}

const passwordField = document.getElementById("show_pass");
const toggleButton = document.getElementById("show");

  toggleButton.addEventListener("click", function () {
    if (passwordField.type === "password") {
      passwordField.type = "text";
      toggleButton.textContent = "Hide Password";
    } else {
      passwordField.type = "password";
      toggleButton.textContent = "Show Password";
    }
  });
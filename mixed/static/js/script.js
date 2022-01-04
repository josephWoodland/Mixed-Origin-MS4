// Materialize functions //
$(document).ready(function(){
    $(".dropdown-trigger").dropdown();
    $('.sidenav').sidenav();
})

// Message container JS //
const message = document.getElementById('message')
const messageClose = document.querySelector('.alert-close')


// Fade out function
function  fadeOut() {

    const fadeEffect = setInterval(function () {
        if (!message.style.opacity) {
            message.style.opacity = 1;
        }
        if (message.style.opacity > 0) {
            message.style.opacity -= 0.1;
        } else {
            clearInterval(fadeEffect);
        }
    }, 20);

}

if (message){
    messageClose.addEventListener('click', fadeOut);
    
}

// Updating the quantity on the product view page //

const upBtn = document.getElementById('btn-plus')
const downBtn = document.getElementById('btn-minus')
const numberInputBox = document.getElementById('number-amount')
const stockNumberAlert = document.getElementById('amount-alert')

if (numberInputBox){

    let currNumber = numberInputBox.value
    let maxNumber = numberInputBox.max
    upBtn.addEventListener('click', function(e){
        e.preventDefault()
    
        if (currNumber < maxNumber) {
            currNumber ++
            numberInputBox.value = currNumber
        }
    
        if (currNumber == maxNumber) {
            stockNumberAlert.classList.remove('hidden')
        }
    })
    
    downBtn.addEventListener('click', function(e){
        e.preventDefault()
        
        if (currNumber >= 1){
            currNumber --
            numberInputBox.value = currNumber
        }
    
        if (currNumber < maxNumber) {
            stockNumberAlert.classList.add('hidden')
        } 
    
    })
}
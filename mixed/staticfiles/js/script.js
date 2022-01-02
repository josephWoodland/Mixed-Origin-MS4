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
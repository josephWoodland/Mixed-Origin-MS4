// Materialize functions //
$(document).ready(function(){
    $(".dropdown-trigger").dropdown();
    $('.sidenav').sidenav();
    $('.tooltipped').tooltip();
})

// Message container JS //
const message = document.getElementById('message')
const messageClose = document.querySelector('.alert-close')


// Fade out function
function  fadeOut() {

    const fadeEffect = setInterval(() => {
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

// Check if message is in the html
if (message){
    messageClose.addEventListener('click', fadeOut);
    // Run the fadeOut function after 3 seconds
    setTimeout(function(){
        fadeOut()
    }, 3000)
}

// Updating the quantity on the product view page //

const upBtn = document.getElementById('btn-plus')
const downBtn = document.getElementById('btn-minus')
const numberInputBox = document.getElementById('order-amount')
const stockNumberAlert = document.getElementById('amount-alert')

if (numberInputBox){

    let currNumber = numberInputBox.value
    let maxNumber = numberInputBox.max
    upBtn.addEventListener('click', (e) => {
        e.preventDefault()
    
        if (currNumber < maxNumber) {
            currNumber ++
            numberInputBox.value = currNumber
        }
    
        if (currNumber == maxNumber) {
            stockNumberAlert.classList.remove('hidden')
        }
    })
    
    downBtn.addEventListener('click', (e) => {
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


// Show the search bar on partners page //

const searchForm = document.getElementById("searchForm")
const searchOpen = document.getElementById("searchOpen")

if (searchOpen) {
    searchOpen.addEventListener("click", (e) => {
        e.preventDefault()
        searchOpen.classList.add("hide")
        searchForm.classList.remove("hide")
    })
}


// Save to later checkbox //

const heart = document.querySelectorAll("#heart")
const checkboxSave = document.querySelectorAll("#saveForLater")

if (heart) {

    heart.forEach(item => {
    // Loop through the array of elements and add an event listener //
        item.addEventListener('click', (e) => {
            e.preventDefault()
            if (item.classList.contains('far')){
                item.classList.remove('far')
                item.classList.add('fas')
                checkboxSave.checked = true;
            } else {
                item.classList.remove('fas')
                item.classList.add('far')
                checkboxSave.checked = false;
            }
    
        })
    }

    )
    
}
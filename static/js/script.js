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
function  fadeOut(el) {

    const fadeEffect = setInterval(() => {
        if (!el.style.opacity) {
            el.style.opacity = 1;
        }
        if (el.style.opacity > 0) {
            el.style.opacity -= 0.1;
        } else {
            clearInterval(fadeEffect);
        }
    }, 20);

}


function  fadeIn(el) {

    const fadeEffect = setInterval(() => {
        if (!el.style.opacity) {
            el.style.opacity = 1;
        }
        clearInterval(fadeEffect);
    }, 50);

}

// Check if message is in the html
if (message){
    messageClose.addEventListener('click', fadeOut);
    // Run the fadeOut function after 3 seconds
    // setTimeout(() => {
    //     fadeOut(message)
    // }, 3000)
}

// Updating the quantity on the product view page by selecting a single element //

const upBtn = document.getElementById('btn-plus')
const downBtn = document.getElementById('btn-minus')
const numberInputBox = document.getElementById('order-amount')
const stockNumberAlert = document.getElementById('amount-alert')

if (numberInputBox) {

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

// Updating the quantity of an item in the cart by looping over an array of elements and traversing the DOM

const plusBtn = document.querySelectorAll('#cart-plus')
const minusBtn = document.querySelectorAll('#cart-minus')

if (plusBtn) {

    plusBtn.forEach(el => {

        el.addEventListener('click', (e) => {
            e.preventDefault()

            let inputBox = el.previousElementSibling
            let curOrderAmount = parseInt(inputBox.value)
            let maxOrderNumber = parseInt(inputBox.max)
            let alert = el.closest('.row').nextElementSibling

            if (curOrderAmount < maxOrderNumber) {
                curOrderAmount ++
                inputBox.value = curOrderAmount
            } 

            if (curOrderAmount == maxOrderNumber) {
                alert.classList.remove('hidden')
            }
        })
    }
    )

    minusBtn.forEach(el => {
        // Loop through the array of elements and add an event listener //
            el.addEventListener('click', (e) => {
                e.preventDefault()

                let inputBox = el.nextElementSibling
                let curOrderAmount = parseInt(inputBox.value)
                let maxOrderNumber = parseInt(inputBox.max)
                let alert = el.closest('.row').nextElementSibling

                if (curOrderAmount >= 1 ) {
                    curOrderAmount --
                    inputBox.value = curOrderAmount
                } 
    
                if (curOrderAmount < maxOrderNumber) {
                    alert.classList.add('hidden')
                }
            })
        }
        )
}


// Popup card for adding items to the cart

const popupCart = document.getElementById("popup")
const itemQuantity = document.getElementById('itemQuantity')
const addToCart = document.getElementById('addToCart')
const form = document.getElementById("form")
const cartNotification = document.getElementById('cartNotification')

if (addToCart) {

    function submitForm(form){
        form.submit()
    }

    addToCart.addEventListener('click', (e) => {
        e.preventDefault()
        curCartAmount = cartNotification.innerText
        itemQty = numberInputBox.value
        itemQuantity.innerText = itemQty
        console.log(itemQty)
        console.log(curCartAmount)
        newCartAmount = parseInt(curCartAmount) + parseInt(itemQty)
        console.log(newCartAmount)
        cartNotification.innerText = newCartAmount

        fadeIn(popupCart)
        
        setTimeout(() => {
            fadeOut(popupCart)
            submitForm(form)
        }, 3000)

    })
}
// Materialize functions //
$(document).ready(function () {
  $(".dropdown-trigger").dropdown();
  $(".sidenav").sidenav();
  $(".tooltipped").tooltip();
});

// Message container JS //
const message = document.getElementById("message");
const messageClose = document.querySelector(".alert-close");

// Fade out function
function fadeOut(el) {
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

function fadeIn(el) {
  const fadeEffect = setInterval(() => {
    if (!el.style.opacity) {
      el.style.opacity = 1;
    }
    clearInterval(fadeEffect);
  }, 50);
}

// Check if message is in the html
if (message) {
  messageClose.addEventListener("click", fadeOut);
  // Run the fadeOut function after 3 seconds
  setTimeout(() => {
    fadeOut(message);
  }, 3000);
}

// Updating the quantity on the product view page by selecting a single element //

const upBtn = document.getElementById("btn-plus");
const downBtn = document.getElementById("btn-minus");
const numberInputBox = document.getElementById("order-amount");
const stockNumberAlert = document.getElementById("amount-alert");

if (numberInputBox) {
  let currNumber = numberInputBox.value;
  let maxNumber = numberInputBox.max;

  upBtn.addEventListener("click", (e) => {
    e.preventDefault();

    if (currNumber < maxNumber) {
      currNumber++;
      numberInputBox.value = currNumber;
    }

    if (currNumber == maxNumber) {
      stockNumberAlert.classList.remove("hidden");
    }
  });

  downBtn.addEventListener("click", (e) => {
    e.preventDefault();

    if (currNumber >= 1) {
      currNumber--;
      numberInputBox.value = currNumber;
    }

    if (currNumber < maxNumber) {
      stockNumberAlert.classList.add("hidden");
    }
  });
}

// Show the search bar on partners page //

const searchForm = document.getElementById("searchForm");
const searchOpen = document.getElementById("searchOpen");

if (searchOpen) {
  searchOpen.addEventListener("click", (e) => {
    e.preventDefault();
    searchOpen.classList.add("hide");
    searchForm.classList.remove("hide");
  });
}

// Save to later checkbox //

const heart = document.querySelectorAll("#heart");
const checkboxSave = document.querySelectorAll("#saveForLater");

if (heart) {
  heart.forEach((item) => {
    // Loop through the array of elements and add an event listener //
    item.addEventListener("click", (e) => {
      e.preventDefault();
      if (item.classList.contains("far")) {
        item.classList.remove("far");
        item.classList.add("fas");
        checkboxSave.checked = true;
      } else {
        item.classList.remove("fas");
        item.classList.add("far");
        checkboxSave.checked = false;
      }
    });
  });
}

// Updating the quantity of an item in the cart by looping over an array of elements and traversing the DOM

const plusBtn = document.querySelectorAll("#cart-plus");
const minusBtn = document.querySelectorAll("#cart-minus");

if (plusBtn) {
  plusBtn.forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();

      let inputBox = el.previousElementSibling;
      let curOrderAmount = parseInt(inputBox.value);
      let maxOrderNumber = parseInt(inputBox.max);
      let alert = el.closest(".row").nextElementSibling;

      if (curOrderAmount < maxOrderNumber) {
        curOrderAmount++;
        inputBox.value = curOrderAmount;
      }

      if (curOrderAmount == maxOrderNumber) {
        alert.classList.remove("hidden");
      }
    });
  });

  minusBtn.forEach((el) => {
    // Loop through the array of elements and add an event listener //
    el.addEventListener("click", (e) => {
      e.preventDefault();

      let inputBox = el.nextElementSibling;
      let curOrderAmount = parseInt(inputBox.value);
      let maxOrderNumber = parseInt(inputBox.max);
      let alert = el.closest(".row").nextElementSibling;

      if (curOrderAmount >= 1) {
        curOrderAmount--;
        inputBox.value = curOrderAmount;
      }

      if (curOrderAmount < maxOrderNumber) {
        alert.classList.add("hidden");
      }
    });
  });
}

// Popup card for adding items to the cart

const popupCart = document.getElementById("popup");
const itemQuantity = document.getElementById("itemQuantity");
const addToCart = document.getElementById("addToCart");
const form = document.getElementById("form");
const hiddenCartNumber = document.getElementById("hiddenCartNumber");
const cartNotificationFirst = document.getElementById("cartNotificationFirst");
const cartNotificationSeen = document.getElementById("cartNotificationSeen");
const productTotal = document.getElementById("productTotal");
const cartTotal = document.getElementById("cartTotal");
const productPriceElement = document.getElementById("productPrice");
const hiddenTotal = document.getElementById("hiddenTotal");

// function to trigger the submit event on a form
function submitForm(form) {
  form.submit();
}

// set the z index of an element
function setZIndex(el) {
  if (el.style.zIndex < 0) {
    el.style.zIndex = "-1000";
  } else {
    el.style.zIndex = "1000";
  }
}

// function to round to 2 decimal places
function round(num) {
  const price = Number(Math.round(num + "e" + 2) + "e-" + 2).toFixed(2);
  return Number(price);
}

// update the cart notification in the nav bar
function upDateCartNotification(itemQty) {
  let curCartAmount;

  if (cartNotificationFirst) {
    cartNotificationFirst.classList.remove("transparent");
  }

  if (hiddenCartNumber.innerText) {
    curCartAmount = hiddenCartNumber.innerText;
  } else {
    curCartAmount = 0;
  }

  itemQuantity.innerText = itemQty;
  let newCartAmount = Number(curCartAmount) + Number(itemQty);

  if (cartNotificationSeen) {
    cartNotificationSeen.innerText = newCartAmount;
  } else {
    cartNotificationFirst.innerText = newCartAmount;
  }
}

// Function to add product to cart
function addProductToCart(itemQty) {
  // Get the order Item total and the product price and work out the total
  let productPrice = parseFloat(productPriceElement.innerText);
  let productTotalPrice = itemQty * productPrice;

  // Get the current cart total
  let curCartTotal = Number(hiddenTotal.innerText);
  // Update the cart notification number
  upDateCartNotification(itemQty);

  // Work out the new total
  let newTotal = curCartTotal + productTotalPrice;

  // Update the HTML
  cartTotal.innerText = round(newTotal);
  productTotal.innerText = round(productTotalPrice);

  setZIndex(popupCart);
  fadeIn(popupCart);
  submitForm(form);

  setTimeout(() => {
    fadeOut(popupCart);
    setZIndex(popupCart);
  }, 2000);
}

// Update the cart information in the popup
if (addToCart) {
  addToCart.addEventListener("click", (e) => {
    e.preventDefault();
    let itemQty = numberInputBox.value;
    addProductToCart(itemQty);
  });
}

// Dropdown menu

const products = document.getElementById("products");
const dropdown = document.getElementById("dropdown-wrapper");

products.addEventListener("mouseenter", () => {
  dropdown.style.display = "grid";
});

products.addEventListener("mouseleave", () => {
  dropdown.style.display = "none";
});

if (dropdown) {
  dropdown.addEventListener("mouseenter", () => {
    dropdown.style.display = "grid";
  });
  dropdown.addEventListener("mouseleave", () => {
    dropdown.style.display = "none";
  });
}

/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

const stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
const clientSecret = $("#id_client_secret").text().slice(1, -1);
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();
const style = {
  base: {
    color: "#000",
    fontFamily: '"Poppins", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4",
    },
  },
  invalid: {
    color: "#b05150",
    iconColor: "#b05150",
  },
};
const card = elements.create("card", { style: style });
card.mount("#card-element");

// Handle realtime validation errors on the card element
card.addEventListener("change", (e) => {
  const errorDiv = document.getElementById("card-errors");
  if (e.error) {
    const html = `
            <span class="error-alert" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span class="error-alert" >${e.error.message}</span>
        `;
    $(errorDiv).html(html);
  } else {
    errorDiv.textContent = "";
  }
});

// Handle form submit

const form = document.getElementById("payment-form");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  card.update({ disabled: true });

  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
      billing,
    },
  });
});

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
const errorDiv = document.getElementById("card-errors");

card.addEventListener("change", (er) => {
  if (er.error) {
    const html = `
            <span class="error-alert" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span class="error-alert" >${er.error.message}</span>
        `;

    $(errorDiv).html(html);
  }
});

// Handle form submit

const paymentForm = document.getElementById("payment-form");
const walletCheckbox = document.getElementById("id_walletDetails");

paymentForm.addEventListener("submit", (e) => {
  e.preventDefault();
  card.update({ disabled: true });
  $("#submit-button").attr("disabled", true);
  $("#loading-overlay").fadeToggle(100);

  const walletDetails = walletCheckbox.checked;
  const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  const postData = {
    csrfmiddlewaretoken: csrfToken,
    client_secret: clientSecret,
    wallet_details: walletDetails,
  };
  const url = "/checkout/cache_checkout_data/";

  $.post(url, postData)
    .done(() => {
      stripe
        .confirmCardPayment(clientSecret, {
          payment_method: {
            card: card,
            billing_details: {
              name: $.trim(form.full_name.value),
              phone: $.trim(form.phone_number.value),
              email: $.trim(form.email.value),
              address: {
                line1: $.trim(form.street_address1.value),
                line2: $.trim(form.street_address2.value),
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                state: $.trim(form.county.value),
              },
              shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                  line1: $.trim(form.street_address1.value),
                  line2: $.trim(form.street_address2.value),
                  city: $.trim(form.town_or_city.value),
                  country: $.trim(form.country.value),
                  postal_code: $.trim(form.postcode.value),
                  state: $.trim(form.county.value),
                },
              },
            },
          },
        })
        .then((response) => {
          if (response.error) {
            const html = `
              <span class="error-alert" role="alert">
                  <i class="fas fa-times"></i>
              </span>
              <span class="error-alert" >${response.error.message}</span>
          `;
            $(errorDiv).html(html);
            card.update({ disabled: false });
            $("#loading-overlay").fadeToggle(100);
            $("#submit-button").attr("disabled", false);
          } else {
            if (response.paymentIntent.status === "succeeded") {
              paymentForm.submit();
            }
          }
        });
    })
    .fail(() => {
      location.reload();
    });
});

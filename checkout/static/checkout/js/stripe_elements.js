var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        border: '#000',
        fontWeight: '500',
        fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4',
            fontSize: '16px',
        },
    },
    invalid: {
        iconColor: '#dc3545',
        color: '#dc3545',
    },
};

var card = elements.create('card', {
    style: style
});
card.mount('#card-element');


// Handing realtime validation errors, taken directly from Boutique Ado

card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
          <span class="icon" role="alert">
              <i class="fas fa-times"></i>
          </span>
          <span>${event.error.message}</span>
      `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit, taken directly from Boutique Ado

var form = document.getElementById('payment-form');
// var form = document.getElementById('payment-form');


form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({
        'disabled': true
    });
    $('#btnSubmit').attr('disabled', true);

    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';
    
    $.post(url, postData).done(function() {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.first_name.value),
                    email: $.trim(form.email.value),
                    phone: $.trim(form.phone.value),
                    address: {
                        line1: $.trim(form.street.value),
                        city: $.trim(form.town.value),
                    }
                }
            },
            shipping: {
                    name: $.trim(form.first_name.value),
                    address: {
                        line1: $.trim(form.street.value),
                        city: $.trim(form.town.value),
                    },
                }
            }).then(function (result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
        <span class="icon" role="alert">
        <i class="fas fa-times"></i>
        </span>
        <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                card.update({
                    'disabled': false
                });
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    console.log(form);
                    form.submit();
                }
            }
        });

    }).fail(function() {
        location.reload();
    });
    });
<script src="https://www.google.com/recaptcha/enterprise.js?render={{ RECAPTCHA_SITE_KEY }}"></script>


document.getElementById('submitBtn').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the default form submit

    grecaptcha.enterprise.execute('{{ RECAPTCHA_SITE_KEY }}', {action: 'contact_us'}).then(function(token) {
        // Add the token to a hidden field
        var inputToken = document.createElement('input');
        inputToken.setAttribute('type', 'hidden');
        inputToken.setAttribute('name', 'g-recaptcha-response');
        inputToken.setAttribute('value', token);
        document.getElementById('contactForm').appendChild(inputToken);

        // Submit the form
        document.getElementById('contactForm').submit();
    });
});
// script.js

window.onbeforeunload = function () {
  window.scrollTo(0, 0);
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contact-form');
    const confirmationMessage = document.getElementById('confirmation-message');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Create FormData object to easily work with form data
        const formData = new FormData(form);

        // Send form data using fetch API
        fetch('/contact', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                form.reset(); // Reset the form fields
                confirmationMessage.classList.remove('d-none'); // Show confirmation message
            } else {
                console.error('Form submission error:', response);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

// The DOMContentLoaded event is used to ensure that your JavaScript code runs only after the HTML document has been fully loaded and parsed, but before all the stylesheets, images, and subframes have finished loading.

document.addEventListener("DOMContentLoaded", function() {
    // Select all message divs
    const messages = document.querySelectorAll(".messages");

        messages.forEach(function(message) {    
        //Checking if message is not very important
        if (!message.querySelector('.alert-danger')){
            // Set a timeout to hide the message
            setTimeout(function() {
                message.style.display = 'none';
            }, 7000); // Change 7000 to the desired time in milliseconds
        }
    }
    );
});


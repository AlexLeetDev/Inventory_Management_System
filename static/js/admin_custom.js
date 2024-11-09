// admin_custom.js

// Run when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    console.log("Custom admin JavaScript loaded!");

    // Display a welcome message on the dashboard
    if (window.location.pathname === '/admin/') {
        alert("Welcome to the customized Django Admin Dashboard!");
    }

    // Create a "Back to Top" button and add it to the page
    const backToTopButton = document.createElement("button");
    backToTopButton.textContent = "Back to Top";
    backToTopButton.className = "button";
    backToTopButton.style.position = "fixed";
    backToTopButton.style.bottom = "20px";
    backToTopButton.style.right = "20px";
    backToTopButton.style.display = "none";
    document.body.appendChild(backToTopButton);

    // Show the "Back to Top" button when scrolled down
    window.addEventListener("scroll", function () {
        if (window.scrollY > 200) {
            backToTopButton.style.display = "block";
        } else {
            backToTopButton.style.display = "none";
        }
    });

    // Scroll back to the top when the "Back to Top" button is clicked
    backToTopButton.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});

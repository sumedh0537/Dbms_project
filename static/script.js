// script.js

// Function to show an alert for non-working features
function showAlert(message) {
    alert(message);
}
function toggleUpdateInput(skill) {
    // Find the form associated with the skill
    const forms = document.querySelectorAll('.update-form');
    forms.forEach(form => {
        // Check if the form's hidden input matches the skill
        if (form.querySelector('input[name="old_skill"]').value === skill) {
            // Toggle the display of the form
            form.style.display = form.style.display === 'none' ? 'flex' : 'none';
        } else {
            // Hide other forms
            form.style.display = 'none';
        }
    });
}
document.addEventListener("DOMContentLoaded", function() {
    // const applyButtons = document.querySelectorAll(".job-item button");
    // applyButtons.forEach(button => {
    //     button.addEventListener("click", function() {
    //         showAlert("This feature is not yet implemented.");
    //     });
    // });

    const searchButton = document.querySelector("#searchBtn");
    searchButton.addEventListener("click", function() {
        showAlert("Search feature is not yet implemented.");
    });

    // Optional: logout toggle for demo purposes (can be kept or removed)
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.onclick = function () {
            const accountDetails = document.getElementById("accountDetails");
            if (accountDetails) accountDetails.style.display = "none";
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
    console.log("Attempting to load navigation..."); // Debugging line

    fetch("navigation.html")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("nav-container").innerHTML = data;
            console.log("Navigation loaded successfully."); // Debugging line
        })
        .catch(error => {
            console.error("Error loading navigation:", error);
            document.getElementById("nav-container").innerHTML = "<p>Error loading navigation</p>";
        });
});

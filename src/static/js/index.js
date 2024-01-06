
const url = "http://127.0.0.1:8000/download";  // Replace with your correct URL

// Wait for the document to be fully loaded before executing JavaScript
const button = document.querySelector('#test-button');

// Add a click event listener to the button
button.addEventListener("click", async () => {
    let response = await fetch(url);
    if (response.ok) {
        let data = await response.json();
        console.log(data);
    }
});

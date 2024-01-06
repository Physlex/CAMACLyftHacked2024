
const url = "http://127.0.0.1:8000/download";  // Replace with your correct URL

// Wait for the document to be fully loaded before executing JavaScript
const button = document.querySelector('#test-button');

// Add a click event listener to the button
button.addEventListener("click", async () => {
    try {
        let response = await fetch(url + '/download');
        if (response.ok) {
            let data = await response.json();
            console.log(data);  // TODO: DO SOMETHING
        } else {
            throw(error);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
});

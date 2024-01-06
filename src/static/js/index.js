
// const url = "https://126.'lakgja[oijga:8000" // TODO: This
// button = document.querySelector('#test-button');
// button.addEventListener("click", () => {
//     let response = fetch(url + '/download', 'GET').then((data) => {
//         return data.json();
//     });
// });
// static/js/main.js

const url = "http://127.0.0.1:8000/download";  // Replace with your correct URL

// Wait for the document to be fully loaded before executing JavaScript
document.addEventListener('DOMContentLoaded', (event) => {
    // Get the button element
    const button = document.querySelector('#test-button');

    // Add a click event listener to the button
    button.addEventListener("click", async () => {
        try {
            // Make a GET request to the '/download' endpoint
            let response = await fetch(url + '/download');
            
            // Check if the request was successful (status code 200)
            if (response.ok) {
                // Parse the JSON response
                let data = await response.json();
                console.log(data);  // Do something with the data
            } else {
                console.error('Failed to fetch data:', response.status, response.statusText);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });
});


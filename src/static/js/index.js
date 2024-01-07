
const url = "http://127.0.0.1:8000";  // Replace with your correct URL

document.querySelector("#connection-btn").addEventListener("click", async (event) => {
    let response = await fetch(url + "/download");
    if (response.ok) {
        let data = await response.json();
        console.log(data);
    }  else {
        console.error('Failed to fetch data:', response.status, response.statusText);
    }
});

document.querySelector("#username-form-btn").addEventListener("submit", async (event) => {
    let userName = document.querySelector('#username-form').value;
    let response = await fetch(url + "/authenticate", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({ variable: userName }),
    });
    if (response.ok) {
        let json_response = await response.json();
        console.log(json_response);
    } else {
        console.error("Failed to fetch data: ", response.status, response.statusText);
    }
});


/// WEBSOCKET

const socket = new WebSocket("ws://localhost:8000/connect");

socket.addEventListener("open", (event) => {
    console.log("Hello Server!");
});

socket.addEventListener("message", (event) => {
    console.log("Message Thing");
});

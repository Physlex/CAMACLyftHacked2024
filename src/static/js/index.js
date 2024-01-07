
document.addEventListener("DOMContentLoaded", () => {
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
        console.log("Connection Established");
    });

    socket.addEventListener("message", (event) => {
        console.log("Generic Message");
    });

    socket.addEventListener("error", (event) => {
        console.error("Websocket Error: ", socket.error)
    });

    socket.addEventListener("close", (event) => {
        console.log("Connection Ended");
    });


    /// CHART

    data = {
        labels: ['X', 'Y', 'Z'],
        datasets: [{
            label: 'Dataset 1',
            borderColor: 'red',
        }, {
            label: 'Dataset 2',
            borderColor: 'green',
        }, {
            label: 'Dataset 3',
            borderColor: 'blue',
        }]
    };

    options = {
        responsive: true,
        maintainAspectRatio: false
    }

    const ctx = document.querySelector('#myChart').getContext('2d');
    let my_chart = new Chart(ctx, {type: 'bar', data: data, options: options});
});


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


    /// CHART

    data = {
        datasets: [{
            label: "Acceleration",
            data: {'X': -2, 'Y': 4, 'Z': 3}
        }, {
            label: "Rotational Velocity",
            data: {'X': -2, 'Y': 4, 'Z': 3}
        },],
    };

    options = {
        responsive: true,
        maintainAspectRatio: false,
    }

    let ctx = document.querySelector('#chart').getContext('2d');
    let mpu_chart = new Chart(ctx, {type: 'bar', data: data, options: options});
    ctx.canvas.style.position = 'relative';
    ctx.canvas.style.height = '60vh';
    ctx.canvas.style.width = '80vw';

    /// WEBSOCKET

    const socket = new WebSocket("ws://localhost:8000/connect");

    socket.addEventListener("open", (event) => {
        console.log("Stream Connection Established To Server");
    });

    socket.addEventListener("message", (event) => {
        console.log("Message From Server: ", event.data);
 
        mpu_chart.update();
    });

    socket.addEventListener("error", (event) => {
        console.error("Websocket Error: ", event.data);
    });

    socket.addEventListener("close", (event) => {
        console.log("Connection Ended To Server");
    });
});

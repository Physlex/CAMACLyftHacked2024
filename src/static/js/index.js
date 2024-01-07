
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


    // usrDisplay = document.querySelector("#username-form-btn");


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
        scales: {
            y: {
                // the data minimum used for determining the ticks is Math.min(dataMin, suggestedMin)
                suggestedMin: -50000,
        
                // the data maximum used for determining the ticks is Math.max(dataMax, suggestedMax)
                suggestedMax: 50000,
            }
        }
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
        read = JSON.parse(event.data);
        console.log("Hi From Server: ", read);

        if(read.usr) { // if this exists, the system just read an NFC. Set up user!
            // console.log("======== NFC ========");
            // console.log("hi");
            // console.log("======== NFC ========");
            // document.querySelector("#username-form-btn").innerHTML = read.usr;
            document.querySelector("#usr").textContent = "Welcome, Cameron!";
        }

        data.datasets[0].data = {"X": parseInt(read["ax"]), "Y": parseInt(read["ay"]), "Z": parseInt(read["az"])};
        data.datasets[1].data = {"X": parseInt(read["gx"]), "Y": parseInt(read["gy"]), "Z": parseInt(read["gz"])};



        // console.log(event.data["ax"]);
 
        mpu_chart.update();
    });

    socket.addEventListener("error", (event) => {
        console.error("Websocket Error: ", event.data);
    });

    socket.addEventListener("close", (event) => {
        console.log("Connection Ended To Server");
    });
});

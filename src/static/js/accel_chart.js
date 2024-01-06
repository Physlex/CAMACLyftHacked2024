// your_script.js
document.addEventListener('DOMContentLoaded', function () {
    // Get the canvas element
    var ctx = document.getElementById('myChart').getContext('2d');

    // Create a bar chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['x', 'Y', 'Z'],
            datasets: [{
                label: 'bs Dataset',
                data: [10, 20, 15],
                backgroundColor: ['red', 'green', 'blue'],
            }]
        }
    });
});

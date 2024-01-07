// // your_script.js
// document.addEventListener('DOMContentLoaded', function () {
//     // Get the canvas element
//     var ctx = document.getElementById('myChart').getContext('2d');

//     // Create a bar chart
//     var myChart = new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: ['x', 'Y', 'Z'],
//             datasets: [{
//                 label: 'bs Dataset',
//                 data: [[10, 20, 15],
//                         [15, 15, 10],
//                         [12, 12, 12]],
//                 backgroundColor: ['red', 'green', 'blue'],
//             }]
//         }
//     });
// });
// your_script.js
document.addEventListener('DOMContentLoaded', function () {
    // Get the canvas element
    var ctx = document.getElementById('myChart').getContext('2d');

    // Create a line chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['x', 'Y', 'Z'],
            datasets: [{
                label: 'Dataset 1',
                data: [10, 20, 15],
                borderColor: 'red',
                backgroundColor: 'transparent',
            }, {
                label: 'Dataset 2',
                data: [15, 15, 10],
                borderColor: 'green',
                backgroundColor: 'transparent',
            }, {
                label: 'Dataset 3',
                data: [12, 12, 12],
                borderColor: 'blue',
                backgroundColor: 'transparent',
            }]
        },
        options: {
            responsive: false,  // Set to false to disable automatic resizing
            maintainAspectRatio: false,  // Set to false to allow custom width and height
            // other options...
        }
    });
});



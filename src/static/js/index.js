
const url = "https://126.'lakgja[oijga:8000" // TODO: This
button = document.querySelector('#test-button');
button.addEventListener("click", () => {
    let response = fetch(url + '/download', 'GET').then((data) => {
        return data.json();
    });
});

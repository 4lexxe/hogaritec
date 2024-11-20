const button = document.getElementById('payButton');
const buttonText = document.getElementById('buttonText');
const loadingOverlay = document.querySelector('.loading-overlay');
const spinner = document.querySelector('.spinner');

button.addEventListener('click', (e) => {
    if (button.disabled) return;

    button.disabled = true;
    buttonText.style.opacity = '0';
    loadingOverlay.style.width = '100%';
    spinner.style.display = 'block';

    setTimeout(() => {
        payment(e)
    }, 1300)

    setTimeout(() => {
        button.disabled = false;
        buttonText.style.opacity = '1';
        loadingOverlay.style.width = '0%';
        spinner.style.display = 'none';
    }, 2000);
});

async function payment(e) {
    data = { id_cart: e.target.value }

    let url = "/payment/create_order"

    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", 'X-CSRFToken': csrftoken },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(data => {
            window.open(data.init_point, "_blank")
        })
        .catch(error => {
            console.log(error)
        })
}
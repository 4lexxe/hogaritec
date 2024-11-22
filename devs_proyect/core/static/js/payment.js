const button = document.getElementById('payButton');
const buttonText = document.getElementById('buttonText');
const loadingOverlay = document.querySelector('.loading-overlay');
const spinner = document.querySelector('.spinner');

button.addEventListener('click', async (e) => {
    if (button.disabled) return;
    button.disabled = true;
    buttonText.style.opacity = '0';
    loadingOverlay.style.width = '100%';
    spinner.style.display = 'block';

    await new Promise(resolve => setTimeout(resolve, 2000)) 
    
    await payment(e);
    
    setTimeout(() => {        

        button.disabled = false;
        buttonText.style.opacity = '1';
        loadingOverlay.style.width = '0%';
        spinner.style.display = 'none';
    }, 2000);
});

async function payment(e) {
    data = { id_cart:  e.target.closest("#payButton").value }

    let url = "/payment/create_order";

    try{
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json", 'X-CSRFToken': csrftoken },
            body: JSON.stringify(data)
        })

        const datar = await response.json();

        window.open(datar.init_point, "_blank")

    }catch(error){
        console.error("Error: ", error)
    }
}
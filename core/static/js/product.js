// Funcion para obeter la cookie llamada csrftoken (Cross-Site Request Forger) que guarda un token unico
// que se genera en cada sesion del usuario.
//Que sirve para seguridad contra ataques CSRF
function getCookie(name) {
    if (!document.cookie) return null;

    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return decodeURIComponent(value);
        }
    }
    return null;
}

const csrftoken = getCookie('csrftoken');

let btnsAdd = document.querySelectorAll(".addToCart-btn")
btnsAdd.forEach(btn => {
    btn.addEventListener("click", addToCart)
})

function addToCart(e) {
    let product_id = e.target.closest(".addToCart-btn").value;
    let url = "/sale/add_to_cart";

    let data = { id: product_id }

    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", 'X-CSRFToken': csrftoken },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(data2=>{
            if(data2){
                showNotification()
            }
        })
        .catch(error => {
            console.log(error)
        })
}

let progressInterval;
const notification = document.getElementById('notification');
const progressBar = notification.querySelector('.progress');
const progressDuration = 1000;

function showNotification() {
    notification.classList.add('show');
    startProgress();
}

function startProgress() {
    let startTime = null;
    resetProgress();

    function animateProgress(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const width = Math.min((elapsed / progressDuration) * 100, 100);
        progressBar.style.width = width + '%';

        if (width < 100) {
            progressInterval = requestAnimationFrame(animateProgress);
        } else {
            setTimeout(() => {
                hideNotification();
            }, 200)
        }
    }

    progressInterval = requestAnimationFrame(animateProgress);
}

function resetProgress() {
    cancelAnimationFrame(progressInterval);
    progressBar.style.width = '0%';
}

function hideNotification() {
    notification.classList.remove('show');
    resetProgress();
}


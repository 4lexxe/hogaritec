
window.addEventListener('load', () => {
    const scrollY = localStorage.getItem('scrollY');
    if (scrollY !== null) {
        window.scrollTo(0, parseInt(scrollY, 10));
        
        localStorage.removeItem('scrollY');
    }
});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const csrftoken = getCookie('csrftoken');

/* Obtiene un array con todos los objetos de las etiqueta con la clase .addToCart-btn */
let btnsAdd = document.querySelectorAll(".addToCart-btn")
let btnsDelete = document.querySelectorAll(".deleteOfTheCart-btn")

/* Lo recorre y les añade el evente click y la funcion addToCart */
btnsAdd.forEach(btn=>{
    btn.addEventListener("click", addToCart)
})

btnsDelete.forEach(btn => {
    btn.addEventListener("click", deleteOfTheCart)
})

function addToCart(e){

    let product_id = e.target.value
    let url = "/sale/add_to_cart";

    let data = {id:product_id}

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        console.log(data)
        if (data.redirect) {
            // Guarda la posición actual de desplazamiento en localStorage
            localStorage.setItem('scrollY', window.scrollY);

            window.location.href = data.redirect;  // Redirige a la URL recibida
            
        }
        
    })
    .catch(error=>{
        console.log(error)
    })
}



function deleteOfTheCart(e){

    let product_id = e.target.value
    let url = "/sale/delete_of_the_cart";

    let data = {id:product_id}

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        console.log(data)
        if (data.redirect) {
            // Guarda la posición actual de desplazamiento en localStorage
            localStorage.setItem('scrollY', window.scrollY);
            window.location.href = data.redirect;  // Redirige a la URL recibida
            
        }
        
    })
    .catch(error=>{
        console.log(error)
    })
}



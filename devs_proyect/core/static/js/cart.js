
window.addEventListener('load', () => {
    const scrollY = localStorage.getItem('scrollY');
    if (scrollY !== null) {
        window.scrollTo({
            top: parseInt(scrollY, 10),
            left: 0,
            behavior: 'smooth' 
        });        
        localStorage.removeItem('scrollY');
    }
});

//Conseguir la cookie
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

/* Obtiene un array con todos los objetos de las etiqueta con la clase .addToCart-btn */

let btnsAdd2 = document.querySelectorAll(".addToCart-btn2");
let btnsDelete = document.querySelectorAll(".deleteFromCart-btn");
let btndDeleteAll = document.querySelectorAll(".deleteProductFromCart");

/* Lo recorre y les añade el evente click y la funcion addToCart */

btnsAdd2.forEach(btn => {
    btn.addEventListener("click", addToCart2)
})

btnsDelete.forEach(btn => {
    btn.addEventListener("click", deleteFromCart)
})

btndDeleteAll.forEach(btn => {
    btn.addEventListener("click", deleteProductFromCart)
})

//Agrega el producto al carrito y recarga la vista del carrito
function addToCart2(e){
    let product_id = e.target.value;
    let url = "/sale/add_to_cart";

    let data = {id:product_id}
    console.log("data", data)

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data => {
        console.log(data)
        if (data.redirect) {
            // Guarda la posición actual de desplazamiento en el localStorage
            localStorage.setItem('scrollY', window.scrollY);
            window.location.href = data.redirect;  // Redirige a la URL recibida
        }
    })
    .catch(error=>{
        console.log(error)
    })
}

function deleteFromCart(e){
    let product_id = e.target.value;
    let url = "/sale/delete_from_cart";
    let data = {id:product_id};

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


function deleteProductFromCart(e){
    product_id = e.target.closest(".deleteProductFromCart").value;
    let url = "/sale/delete_product_from_cart";
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



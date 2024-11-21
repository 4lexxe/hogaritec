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

//Seleccionar las etiquetas con la clase addToCart-btn y capturar los evento de click
let btnsAdd = document.querySelectorAll(".addToCart-btn")
btnsAdd.forEach(btn=>{
    btn.addEventListener("click", addToCart)
})

function addToCart(e){
    let product_id = e.target.closest(".addToCart-btn").value;
    let url = "/sale/add_to_cart";

    let data = {id:product_id}
    
    console.log("data", data)

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .catch(error=>{
        console.log(error)
    })
}



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

//Funcion para actualizar la data del carrito
async function update(data) {
    console.log(data)
    
    productId = data.cartitem.product
    cartId = data.cart.id

    document.getElementById(`num_of_items${ cartId }`).innerHTML = data.cart.num_of_items
    document.getElementById(`total_price${ cartId }`).innerHTML = "$ " + data.cart.total_price
    document.getElementById(`total_price${ cartId }2`).innerHTML = "$ " +  data.cart.total_price

    if(data.cartitem.id == null){
        document.getElementById(`cartitem${ data.cartitem.product }`).style.display = "none"
        return
    }

    const getFinalPrice = document.getElementById(`get_final_price${ productId }`)
    const quantity = document.getElementById(`quantity${ productId }`)
    const finalPrice = document.getElementById(`final_price${ productId }`)

    getFinalPrice.innerHTML = "$ " + data.cartitem.get_final_price
    quantity.innerHTML = data.cartitem.quantity
    finalPrice.innerHTML = "$ " + data.cartitem.final_price
    
}


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

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data2 => {
        update(data2)
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
    .then(data2 =>{
        update(data2)
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
    .then(data2=>{
        update(data2)
    })
    .catch(error=>{
        console.log(error)
    })
}



$('.btnAddCart').on('click', function () {
    console.log('Logueado');
    var user = this.dataset.user;
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log(user);
    if (user == 'AnonymousUser') {
        console.log('Usuario no autenticado')
    } else {
        addCart(user, productId, action)
    }
})

function addCart(user, productId, action) {
    console.log('Usuario ID: ', user, 'Producto ID: ', productId, 'Accion: ', action)
    var url = '/carrito_add/'

    fetch(url,{
        method: 'post',
        headers: {'Content-Type':'application/json',
        },
        body: JSON.stringify({'user': user, 'productId': productId, 'action': action})
    })
        .then((response)=>{
            return response.json();
        })
        .then((data)=>{
            console.log('data: ', data)
        })
}
;
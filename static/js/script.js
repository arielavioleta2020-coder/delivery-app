// static/js/script.js

// Función que se ejecuta cuando la página está completamente cargada
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página de delivery cargada correctamente');
    
    // Ocultar automáticamente los mensajes de alerta después de 3 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.display = 'none';
        });
    }, 3000);
});

// Función para actualizar cantidades en el carrito
function actualizarCantidad(itemId, cantidad) {
    console.log('Actualizando producto:', itemId, 'Cantidad:', cantidad);
    
    // Aquí iría código para hacer peticiones AJAX al servidor
}

// Función para mostrar/ocultar elementos
function toggleElement(id) {
    const element = document.getElementById(id);
    if (element) {
        if (element.style.display === 'none') {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
    }
}

// Función auxiliar para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

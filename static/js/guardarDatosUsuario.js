function registrarUsuario(event) {
    event.preventDefault();  // Evita el envío tradicional del formulario

    // Llama a la función de validación de JavaScript
    if (!validarFormulario()) {
        return;
    }
    // Llama a la función de validación de edad
    if (!validarEdad()) {
        return;
    }

    document.getElementById('fecha_registro').value = new Date().toISOString().slice(0, 10);

    var formData = new FormData(document.getElementById('registroForm'));

    fetch('/registro', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registro exitoso');
            window.location.href = '/login';  // Redirige al login
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error. Por favor, inténtalo de nuevo.');
    });
}

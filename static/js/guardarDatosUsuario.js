function guardarDatosUsuario() {
    // Recolecta los datos del formulario
    var nombre = document.getElementById('nombre').value;
    var apellido = document.getElementById('apellido').value;
    var username = document.getElementById('username').value;
    var fechaNacimiento = document.getElementById('fecha_nacimiento').value;
    var genero = document.querySelector('input[name="genero"]:checked').value;
    var pais = document.getElementById('pais').value;
    var otroPais = document.getElementById('otro_pais').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // Crea un objeto con los datos del usuario
    var datosUsuario = {
        nombre: nombre,
        apellido: apellido,
        username: username,
        fechaNacimiento: fechaNacimiento,
        genero: genero,
        pais: pais === 'OTRO' ? otroPais : pais, // Si el usuario selecciona 'Otro', usa el valor de otroPais
        email: email,
        password: password // Se guarda la contraseña del usuario
    };

    // Guarda los datos del usuario en localStorage
    localStorage.setItem('datosUsuario', JSON.stringify(datosUsuario));

    // Redirecciona al usuario a otra página después de guardar los datos
    window.location.href = "./login.html";
}

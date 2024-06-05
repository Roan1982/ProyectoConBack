function validarCredenciales() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Recupera los datos del usuario almacenados en localStorage
    var datosUsuario = localStorage.getItem('datosUsuario');
    if (datosUsuario) {
        datosUsuario = JSON.parse(datosUsuario);
        
        // Comprueba si las credenciales ingresadas coinciden con los datos almacenados
        if ((username === datosUsuario.email || username === datosUsuario.username) &&
            password === datosUsuario.password) {
            // Si las credenciales son válidas, redirige al usuario a la página de bienvenida
            window.location.href = "./bienvenido.html";

            // Actualiza la visibilidad de los enlaces en el menú de navegación
            localStorage.setItem('isAuthenticated', 'true');
            actualizarVisibilidadEnlaces();

            return; // Importante: salir de la función aquí para evitar la redirección no deseada
        }
    }

    // Si las credenciales son incorrectas o no hay datos de usuario almacenados, muestra un mensaje de error
    alert("Credenciales incorrectas. Por favor, inténtalo de nuevo.");
}

function logout() {
    // Elimina la autenticación almacenada en localStorage
    localStorage.removeItem('isAuthenticated');

    // Redirige al usuario a la página de inicio de sesión u otra página deseada
    window.location.href = "./login.html"; // Cambia "./login.html" por la URL de tu página de inicio de sesión
}

document.addEventListener("DOMContentLoaded", function() {
    // Verifica si el usuario está autenticado consultando localStorage
    var isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

    // Actualiza la visibilidad de los enlaces en el menú de navegación según el estado de autenticación
    if (isAuthenticated) {
        document.getElementById("bienvenidoLink").style.display = "inline";
        document.getElementById("loginLink").style.display = "none";
        document.getElementById("signupLink").style.display = "none";
        document.getElementById("logoutLink").style.display = "inline"; // Mostrar enlace de logout
    } else {
        document.getElementById("bienvenidoLink").style.display = "none";
        document.getElementById("loginLink").style.display = "inline";
        document.getElementById("signupLink").style.display = "inline";
        document.getElementById("logoutLink").style.display = "none"; // Ocultar enlace de logout
    }
});
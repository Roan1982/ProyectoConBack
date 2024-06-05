
    function submitEmail() {
        var email = document.getElementById("e-mail").value;
    if (email.trim() === "") {
        alert("Por favor, ingresa tu correo electrónico.");
        return;
    }

    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!emailPattern.test(email)) {
        alert("Por favor, ingresa un correo electrónico válido.");
        return;
    }
        // Mostrar la leyenda
        document.getElementById("envio-de-link").style.display = "block";
        // Ocultar el campo de email y el botón
        document.getElementById("e-mail").style.display = "none";
    document.getElementById("submit-email").style.display = "none";
    document.getElementById("email-label").style.display = "none";
    }

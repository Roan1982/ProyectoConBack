
    function mostrarAlerta(mensaje, campo) {
        var alerta = document.createElement("div");
        alerta.className = "alerta";
        alerta.textContent = mensaje;

        campo.classList.add("error");
        campo.parentNode.insertBefore(alerta, campo.nextSibling);
    }

    function limpiarAlerta(campo) {
        campo.classList.remove("error");
        var alerta = campo.parentNode.querySelector(".alerta");
        if (alerta) {
            alerta.parentNode.removeChild(alerta);
        }
    }

    function validarFormulario() {
        var campos = document.querySelectorAll('input[required], select[required]');
        var valido = true;

        campos.forEach(function (campo) {
            if (!campo.value.trim()) {
                mostrarAlerta("Falta completar este campo", campo);
                valido = false;
            }
        });

        var paisSeleccionado = document.getElementById("pais").value;
        var otroPais = document.getElementById("otro_pais").value;

        if (paisSeleccionado === "OTRO" && otroPais.trim() === "") {
            mostrarAlerta("Por favor ingresa tu país", document.getElementById("otro_pais"));
            valido = false;
        }

        var email = document.getElementById("email").value;
        var username = document.getElementById("username").value;

        var emailsRegistrados = ["usuario1@example.com", "usuario2@example.com"];
        var usernamesRegistrados = ["usuario1", "usuario2"];

        if (emailsRegistrados.includes(email)) {
            var campoEmail = document.getElementById("email");
            mostrarAlerta("Este E-mail ya está registrado", campoEmail);
            valido = false;
        }

        if (usernamesRegistrados.includes(username)) {
            var campoUsername = document.getElementById("username");
            mostrarAlerta("Este nombre de usuario no está disponible, por favor elige otro", campoUsername);
            valido = false;
        }

        if (!validarContraseñas()) {
            valido = false;
        }

        return valido;
    }

    function validarContraseñas() {
        var password = document.getElementById("password").value;
        var confirmarPassword = document.getElementById("confirm_password").value;

        if (!validarFormatoContraseña(password)) {
            var campoPassword = document.getElementById("password");
            mostrarAlerta("La contraseña debe tener al menos 8 caracteres, contar con al menos una mayúscula, una minúscula, un número y un caracter especial", campoPassword);
            return false;
        }

        if (password !== confirmarPassword) {
            var campoConfirmPassword = document.getElementById("confirm_password");
            mostrarAlerta("Las contraseñas no coinciden", campoConfirmPassword);
            return false;
        }

        return true;
    }

    function validarFormatoContraseña(password) {
        var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        return regex.test(password);
    }



    function mostrarOtroPais(valor) {
        var otroPaisGroup = document.getElementById("otroPaisGroup");
        if (valor === "OTRO") {
            otroPaisGroup.style.display = "block";
        } else {
            otroPaisGroup.style.display = "none";
        }
    }

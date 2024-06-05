function validarEdad() {
    var input = document.getElementById("fecha_nacimiento");
    var fechaNacimiento = new Date(input.value);
    var fechaLimite = new Date('2011-12-31'); // Fecha límite: 31 de diciembre de 2011
    var hoy = new Date();
    
    if (fechaNacimiento > hoy || fechaNacimiento > fechaLimite) {
        alert("Debes ser mayor de 13 años para registrarte");
        return false; // Evita que el formulario se envíe si la validación falla
    }
    
    return true; // Permite que el formulario se envíe si la validación es exitosa
}
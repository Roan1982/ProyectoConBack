const imagenPasillo2 = document.getElementById('imagen-pasillo2');
    const imagenPasillo3 = document.getElementById('imagen-pasillo3');

    // Función para mostrar la imagen 2 y ocultar la imagen 3
    function mostrarPasillo2() {
        imagenPasillo2.classList.add('active');
        imagenPasillo3.classList.remove('active');
    }

    // Función para mostrar la imagen 3 y ocultar la imagen 2
    function mostrarPasillo3() {
        imagenPasillo3.classList.add('active');
        imagenPasillo2.classList.remove('active');
    }

    // Mostrar pasillo 2 al cargar la página
    mostrarPasillo2();

    // Después de 5 segundos, mostrar pasillo 3 automáticamente
    setTimeout(mostrarPasillo3, 5000); // 5000 milisegundos = 5 segundos













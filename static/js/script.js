function toggleFloatingContainer() {
    const container = document.getElementById('opinion-container');
    container.classList.toggle('active');
}

function submitOpinion() {
    const opinionTextarea = document.getElementById("opinion");
    const opinion = opinionTextarea.value;
    const rating = document.querySelector('.star.active').getAttribute("data-value");
    console.log("Opinión:", opinion);
    console.log("Rating:", rating);
    // Aquí puedes enviar la opinión y la calificación a tu servidor para procesarlas
    // También puedes realizar otras acciones como mostrar un mensaje de confirmación al usuario
}

document.addEventListener("DOMContentLoaded", function() {
    const stars = document.querySelectorAll(".star");
    const opinionTextarea = document.getElementById("opinion");
    const submitOpinionBtn = document.getElementById("submit-opinion");

    let rating = 0;

    stars.forEach(star => {
        star.addEventListener("click", function() {
            const value = parseFloat(star.getAttribute("data-value"));
            if (value === rating) {
                rating = 0;
            } else {
                rating = value;
            }
            highlightStars();
        });
    });

    submitOpinionBtn.addEventListener("click", function() {
        const opinion = opinionTextarea.value;
        console.log("Opinión:", opinion);
        console.log("Rating:", rating);
        // Aquí puedes enviar la opinión y la calificación a tu servidor para procesarlas
        // También puedes realizar otras acciones como mostrar un mensaje de confirmación al usuario
    });

    function highlightStars() {
        stars.forEach(star => {
            const value = parseFloat(star.getAttribute("data-value"));
            if (value <= rating) {
                star.classList.add("active");
            } else {
                star.classList.remove("active");
            }
        });
    }
});

    function toggleFloatingContainer() {
        document.getElementById("floating-container").classList.toggle
("open");
    }
    function submitOpinion() {
        const opinionContainer = document.getElementById
("opinion-container");
        const submitButton = document.getElementById("submit-opinion");
        const thankYouMessage = document.getElementById
("thank-you-message");
        opinionContainer.style.display = "none";
        submitButton.style.display = "none";
        thankYouMessage.style.display = "block";
    }
    document.querySelectorAll(".star").forEach(star => {
        star.addEventListener("click", () => {
            const value = parseInt(star.getAttribute("data-value"));
            document.querySelectorAll(".star").forEach(s => {
                const sValue = parseInt(s.getAttribute("data-value"));
                if (sValue <= value) {
                    s.classList.add("active");
                } else {
                    s.classList.remove("active");
                }
            });
        });
    });

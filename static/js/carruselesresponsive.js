document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel');
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let currentIndex = 0;
  
    function showSlide(index) {
      if (index < 0 || index >= totalSlides) return;
      currentIndex = index;
      const offset = -currentIndex * 100;
      carousel.style.transform = `translateX(${offset}%)`;
    }
  
    // Mostrar siguiente slide
    function nextSlide() {
      showSlide(currentIndex + 1);
    }
  
    // Mostrar slide anterior
    function prevSlide() {
      showSlide(currentIndex - 1);
    }
  
    // Puedes agregar controles de siguiente y anterior
  
    // setInterval(nextSlide, 5000); // Activar para habilitar el autoplay
  });
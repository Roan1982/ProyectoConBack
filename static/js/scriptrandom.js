// Ruta de la carpeta que contiene los archivos PDF
var carpetaPDF = "/static/libros/random/";

// Array de nombres de archivos PDF
var archivosPDF = [
  "EL PATITO FEO.pdf",
  "PULGARCITA.pdf",
  "Rapunzel.pdf",
  "La Sombra.pdf",
  "La tempestad.pdf",
  "LABELLAYLABESTIA.pdf",
  "Las habichuelas mágicas.pdf",
  "Las hadas.pdf",
  "leyenda arbol navidad.pdf",
  "Los fantasmas de Scrooge.pdf",
  "Mark Twain - El robo del elefante blanco.pdf",
  "Mark Twain - Las aventuras de Huckleberry Finn.pdf",
  "Mark Twain - Tom Sawyer b.pdf",
  "Mary Read.pdf",
  "Merlín el Mago.pdf",
  "MiCuentoFantasticoprimaria.pdf",
  "Miguel Cane - Juvenilia.pdf",
  "NubeLluvia.pdf",
  "Parábola.pdf",
  "Peter Pan.pdf",
  "PULGARCITA.pdf",
  "Quiroga, Horacio - Cuentos de la selva.pdf",
  "Rainer Maria Rilke - Cuentos.pdf",
  "Rapunzel.pdf",
  "Ray Bradbury - Crónicas marcianas (selección).pdf",
  "Ray Bradbury - Cuento de navidad.pdf",
  "Ray Bradbury - El cohete.pdf",
  "Ray Bradbury - El dragon.pdf",
  "Ray Bradbury - El flautista.pdf",
  "Ray Bradbury - Encuentro nocturno.pdf",
  "Ray Bradbury - La Sirena.pdf",
  "RelatosPueblo (1).pdf",
  "Ruisenor (1).pdf",
  "Sirenita.pdf",
  "Stephen King - POPSY.pdf",
  "Stephen King- Historias fantásticas II.pdf",
  "Tomas de Iriarte - Fábulas Literarias.pdf",
  "Una Princesa De Marte.pdf",
  "Varios - Mitología universal.pdf",
  "Zenana.pdf"
];


// Función para abrir un archivo PDF aleatorio
function abrirPDF() {
    // Seleccionar un nombre de archivo aleatorio
    var archivoAleatorio = archivosPDF[Math.floor(Math.random() * archivosPDF.length)];
    // Crear la ruta completa al archivo PDF
    var rutaCompleta = carpetaPDF + archivoAleatorio;
    // Redirigir la página al archivo PDF
    window.open(rutaCompleta, '_blank');
}

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth' // Desplazamiento suave
  });
}
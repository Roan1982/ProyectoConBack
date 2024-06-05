const nodemailer = require('nodemailer');

// Configuración del transporte para enviar correos electrónicos
const transporter = nodemailer.createTransport({
    service: 'gmail.com', // Por ejemplo, 'gmail'
    auth: {
        user: 'proyecto.biblioteca.infantil@gmail.com', // Cambia esto por tu dirección de correo electrónico
        pass: 'Codoacodo80!', // Cambia esto por tu contraseña
    },
});

// Función para enviar correos electrónicos
function enviarCorreo(emailDestino, asunto, contenido) {
    const mailOptions = {
        from: 'proyecto.biblioteca.infantil@gmail.com', // Cambia esto por tu dirección de correo electrónico
        to: emailDestino,
        subject: asunto,
        html: contenido,
    };

    transporter.sendMail(mailOptions, function(error, info) {
        if (error) {
            console.error('Error al enviar el correo electrónico:', error);
        } else {
            console.log('Correo electrónico enviado:', info.response);
        }
    });
}

// Llamada a la función para enviar correo electrónico
enviarCorreo('correo-destino@example.com', 'Restet Password', 'Hola! has olvidado tu contraseña, así que te ayudaremos a establecer una nueva. Haz click en el siguiente link y configura tu password nueva. <a href="http://127.0.0.1:5502/Templates/restablecer_password.html">Restablecer Password</a>.');
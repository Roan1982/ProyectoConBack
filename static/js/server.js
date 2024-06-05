const express = require('express');
const nodemailer = require('nodemailer');
const bodyParser = require('body-parser');
const mailPassword = require('./mailPassword');

const app = express();
const port = 3000;

// Middleware para parsear el cuerpo de las solicitudes
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Configuración del transporte para enviar correos electrónicos
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: 'proyecto.biblioteca.infantil@gmail.com', // Cambia esto por tu dirección de correo electrónico
        pass: 'Codoacodo80!', // Cambia esto por tu contraseña
    },
});

// Ruta para manejar la solicitud de envío de correo electrónico
app.post('/enviar-correo', (req, res) => {
    const { emailDestino, asunto, contenido } = req.body;

    // Opciones del correo electrónico
    const mailOptions = {
        from: 'proyecto.biblioteca.infantil@gmail.com', // Cambia esto por tu dirección de correo electrónico
        to: emailDestino,
        subject: asunto,
        html: contenido,
    };

    // Envío del correo electrónico
    transporter.sendMail(mailOptions, function(error, info) {
        if (error) {
            console.error('Error al enviar el correo electrónico:', error);
            res.status(500).send('Error al enviar el correo electrónico');
        } else {
            console.log('Correo electrónico enviado:', info.response);
            res.send('Correo electrónico enviado correctamente');
        }
    });
});

// Iniciar el servidor
app.listen(port, () => {
    console.log(`Servidor escuchando en http://localhost:${port}`);
});
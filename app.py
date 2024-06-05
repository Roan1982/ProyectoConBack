from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
import pymysql
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash
from entidades.models import db, Usuario, Autor, GeneroLiterario, Libro, Opinion


app = Flask('proyecto_Biblioteca')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
bcrypt = Bcrypt(app)
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='biblioteca',
    cursorclass=pymysql.cursors.DictCursor
)
db = pymysql.connect(host="localhost", user="root", password="", database="biblioteca")
cursor = db.cursor()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bienvenido')
def bienvenido():
    # Check if user is logged in (optional for additional security)
    if 'username' not in session:
        flash('Necesitas estar logueado para acceder a esta página.', 'warning')
        return redirect(url_for('login'))

    return render_template('bienvenido.html')

@app.route('/home')
def home():
    return render_template('home.html')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        with connection.cursor() as cursor:
            sql = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):  # Assuming the password field in your table is named 'password'
            session['username'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('bienvenido'))
        else:
            flash('username or password inválido.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('Cerraste sesión de manera exitosa.', 'success')
    return redirect(url_for('index'))

# @app.route('/restablecer_password')
# def restablecer_password():
#     return render_template('restablecer_password.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/tucuento')
def tucuento():
    return render_template('tucuento.html')

@app.route('/submit_story', methods=['POST'])
def submit_story():
    titulo = request.form['titulo']
    opinion = request.form['opinion']
    autor = request.form['autor']
    edad = request.form['edad']

    historia = f"Título: {titulo}\nAutor: {autor}\nEdad: {edad}\nHistoria: {opinion}\n\n"
    
    with open('historias.txt', 'a', encoding='utf-8') as file:
        file.write(historia)
    
    return redirect(url_for('home'))




@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    username = request.form['username']
    email = request.form['email']
    fecha_nacimiento = request.form['fecha_nacimiento']
    genero = request.form['genero']
    pais = request.form['pais']
    if pais == 'OTRO':
        pais = request.form['otro_pais']
    password = request.form['password']
    
    # Convertir fechas a formatos correctos
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
    fecha_registro = request.form['fecha_registro']
    
    # Encriptar la contraseña
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


    # Inserta los datos en la base de datos
    sql = "INSERT INTO usuarios (nombre, apellido, username, email, fecha_nacimiento, fecha_registro, genero, pais, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (nombre, apellido, username, email, fecha_nacimiento, fecha_registro, genero, pais, hashed_password)
    try:
        cursor.execute(sql, val)
        db.commit()
        return jsonify(success=True)
    except pymysql.MySQLError as e:
        print(f"Error al insertar en la base de datos: {e}")
        db.rollback()
        return jsonify(success=False, message=str(e))
    
        
app.secret_key = 'ClaveSecretaDeAppSecretKey'


@app.route('/restablecer_password', methods=['GET', 'POST'])
def restablecer_password():
    return render_template('restablecer_password.html')


if __name__ == '__main__':
    app.run(debug=True)

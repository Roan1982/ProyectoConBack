from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, g
import pymysql
from functools import wraps
from datetime import datetime
from flask_bcrypt import Bcrypt, check_password_hash
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER_IMG = 'static/img/'  # Carpeta donde se almacenarán las imágenes subidas
UPLOAD_FOLDER_PDF = 'static/Libros/'  # Carpeta donde se almacenarán los PDFs subidos
ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS_PDF = {'pdf'}

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    """Format a datetime object."""
    return value.strftime(format)

app = Flask('proyecto_Biblioteca')
app.config['UPLOAD_FOLDER_IMG'] = UPLOAD_FOLDER_IMG
app.config['UPLOAD_FOLDER_PDF'] = UPLOAD_FOLDER_PDF
bcrypt = Bcrypt(app)

@app.template_filter('datetimeformat')
def datetimeformat_filter(value, format='%Y-%m-%d %H:%M:%S'):
    """Format a datetime object."""
    return value.strftime(format)

app.jinja_env.filters['datetimeformat'] = datetimeformat


# Verificar si la extensión del archivo es permitida
def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Configuración de la conexión a la base de datos (ajusta los datos según tu configuración)
db = pymysql.connect(host="sql10.freemysqlhosting.net", user="sql10717364", password="HlNjFFaxiM", database="sql10717364")
cursor = db.cursor()



def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if session.get('rol') in roles:
                return view_func(*args, **kwargs)
            else:
                flash('No tienes permisos para acceder a esta página.', 'error')
                return redirect(url_for('index'))
        return wrapper
    return decorator

# Rutas principales de la aplicación
# Ejemplo de rutas protegidas por roles
@app.route('/admin')
@role_required(['admin'])
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/perfil')
@role_required(['user', 'admin'])
def user_profile():
    # Aquí asumes que tienes acceso a los datos del usuario desde la sesión o una base de datos
    username = session.get('username')  # Obtén el nombre de usuario desde la sesión
    rol = session.get('rol')  # Obtén el rol desde la sesión
    nombre = session.get('nombre')  # Ejemplo: obtener el nombre del usuario desde la sesión
    apellido = session.get('apellido')  # Ejemplo: obtener el apellido del usuario desde la sesión
    email = session.get('email')  # Ejemplo: obtener el email del usuario desde la sesión

    return render_template('user_profile.html', username=username, rol=rol, nombre=nombre, apellido=apellido, email=email)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bienvenido')
def bienvenido():
    if 'username' in session:
        return render_template('bienvenido.html')
    else:
        flash('Inicia sesión para acceder a esta página.', 'error')
        return redirect(url_for('login'))

@app.route('/home')
def home():
    print(session)  # Añadir esta línea para verificar el contenido de la sesión
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('index'))

@app.route('/restablecer_password')
def restablecer_password():
    return render_template('restablecer_password.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/tucuento')
def tucuento():
    return render_template('tucuento.html')

# Funcionalidad para enviar una historia
@app.route('/submit_story', methods=['POST'])
def submit_story():
    titulo = request.form['titulo']
    opinion = request.form['opinion']
    autor = request.form['autor']
    edad = request.form['edad']

    historia = f"Título: {titulo}\nAutor: {autor}\nEdad: {edad}\nHistoria: {opinion}\n\n"
    
    with open('historias.txt', 'a', encoding='utf-8') as file:
        file.write(historia)
    
    flash('Historia enviada correctamente.', 'success')
    return redirect(url_for('home'))


@app.route('/registro', methods=['POST'])
def registro():
    try:
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
        fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Encriptar la contraseña
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
        # Rol predeterminado (2 para usuario, por ejemplo)
        rol_id = 2
        
        # Insertar los datos en la base de datos
        sql = "INSERT INTO usuarios (nombre, apellido, username, email, fecha_nacimiento, fecha_registro, genero, pais, password, rol_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (nombre, apellido, username, email, fecha_nacimiento, fecha_registro, genero, pais, hashed_password, rol_id)
        
        # Conexión a la base de datos (debes establecer previamente la conexión `db`)
        cursor = db.cursor()
        cursor.execute(sql, val)
        db.commit()
        
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return {'success': True}  # Respondemos con éxito al cliente

    except pymysql.MySQLError as e:
        print(f"Error al insertar en la base de datos: {e}")
        db.rollback()
        flash('Error al registrar. Inténtalo nuevamente.', 'error')
        return {'success': False, 'message': 'Error al registrar. Inténtalo nuevamente.'}

@app.route('/libros_seccion', defaults={'genero_id': None})
@app.route('/libros_seccion/<int:genero_id>')
def libros_seccion(genero_id):
    cursor = g.db.cursor()
    if genero_id:
        # Consulta los libros de la base de datos según la sección (género)
        sql = """
        SELECT l.libro_id, l.titulo, a.nombre, a.apellidos, l.imagen, l.resenia, l.pdf, g.nombre AS genero
        FROM libros l
        JOIN autores a ON l.autor_id = a.autor_id
        JOIN generos_literarios g ON l.genero_id = g.genero_id
        WHERE l.genero_id = %s
        """
        cursor.execute(sql, (genero_id,))
    else:
        # Consulta todos los libros si no se ha seleccionado un género
        sql = """
        SELECT l.libro_id, l.titulo, a.nombre, a.apellidos, l.imagen, l.resenia, l.pdf, g.nombre AS genero
        FROM libros l
        JOIN autores a ON l.autor_id = a.autor_id
        JOIN generos_literarios g ON l.genero_id = g.genero_id
        """
        cursor.execute(sql)
    
    libros = cursor.fetchall()
    
    # Obtener el nombre del género si se seleccionó uno
    genero = None
    if genero_id:
        cursor.execute("SELECT nombre FROM generos_literarios WHERE genero_id = %s", (genero_id,))
        genero = cursor.fetchone()
    
    return render_template('libros_seccion.html', libros=libros, genero=genero)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Consulta SQL con join para obtener el rol
        sql = """
            SELECT u.username, u.password, u.nombre, u.apellido, u.email, r.nombre as rol 
            FROM usuarios u 
            JOIN roles r ON u.rol_id = r.id 
            WHERE u.username = %s
        """
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        
        if result:
            stored_username, hashed_password, nombre, apellido, email, rol = result
            
            # Verificar si la contraseña proporcionada coincide con la almacenada
            if check_password_hash(hashed_password, password):
                # Establecer la sesión del usuario con sus datos y rol
                session['username'] = stored_username
                session['rol'] = rol  # Asignar el rol del usuario desde la base de datos
                session['nombre'] = nombre
                session['apellido'] = apellido
                session['email'] = email
                
                flash(f'Inicio de sesión como {session["rol"]}.', 'success')
                
                if 'admin' in session['rol']:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('bienvenido'))
        
        flash('Nombre de usuario o contraseña incorrectos.', 'error')
        return redirect(url_for('login'))
    
    return render_template('login.html')



@app.route('/libros')
def listar_libros():
    cursor.execute("SELECT l.libro_id, l.titulo, a.nombre, a.apellidos, g.nombre_genero, l.año_publicacion, l.imagen, l.resenia, l.pdf FROM libros l JOIN autores a ON l.autor_id = a.autor_id JOIN generos_literarios g ON l.genero_id = g.genero_id")
    libros = cursor.fetchall()
    libros_con_objetos = []
    for libro in libros:
        libro_objeto = {
            'libro_id': libro[0],
            'titulo': libro[1],
            'nombre_autor': f"{libro[2]} {libro[3]}",
            'nombre_genero': libro[4],
            'año_publicacion': libro[5],
            'imagen': libro[6],
            'resenia': libro[7],
            'pdf': libro[8]
        }
        libros_con_objetos.append(libro_objeto)

    return render_template('listar_libros.html', libros=libros_con_objetos)

# Ruta para agregar libros
@app.route('/agregar_libro', methods=['GET', 'POST'])
def agregar_libro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor_id = request.form['autor_id']
        genero_id = request.form['genero_id']
        año_publicacion = request.form['año_publicacion']
        resenia = request.form['resenia']
        
        # Manejo de la imagen subida
        imagen = None
        if 'imagen' in request.files:
            file_img = request.files['imagen']
            if file_img and allowed_file(file_img.filename, ALLOWED_EXTENSIONS_IMG):
                filename_img = secure_filename(file_img.filename)
                file_img.save(os.path.join(app.config['UPLOAD_FOLDER_IMG'], filename_img))
                imagen = os.path.join(app.config['UPLOAD_FOLDER_IMG'], filename_img)
        
        # Manejo del PDF subido
        pdf = None
        if 'pdf' in request.files:
            file_pdf = request.files['pdf']
            if file_pdf and allowed_file(file_pdf.filename, ALLOWED_EXTENSIONS_PDF):
                filename_pdf = secure_filename(file_pdf.filename)
                file_pdf.save(os.path.join(app.config['UPLOAD_FOLDER_PDF'], filename_pdf))
                pdf = os.path.join(app.config['UPLOAD_FOLDER_PDF'], filename_pdf)
        
        sql = "INSERT INTO libros (titulo, autor_id, genero_id, año_publicacion, imagen, resenia, pdf) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (titulo, autor_id, genero_id, año_publicacion, imagen, resenia, pdf)
        cursor.execute(sql, val)
        db.commit()
        flash('Libro agregado correctamente.', 'success')
        return redirect(url_for('listar_libros'))
    
    cursor.execute("SELECT autor_id, CONCAT(nombre, ' ', apellidos) as nombre_completo FROM autores")
    autores = cursor.fetchall()
    cursor.execute("SELECT genero_id, nombre_genero FROM generos_literarios")
    generos = cursor.fetchall()
    return render_template('agregar_libro.html', autores=autores, generos=generos)

@app.route('/editar_libro/<int:libro_id>', methods=['GET', 'POST'])
def editar_libro(libro_id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor_id = request.form['autor_id']
        genero_id = request.form['genero_id']
        año_publicacion = request.form['año_publicacion']
        resenia = request.form['resenia']
        
        # Manejo de la imagen subida
        imagen = None
        if 'imagen' in request.files:
            file_img = request.files['imagen']
            if file_img and allowed_file(file_img.filename, ALLOWED_EXTENSIONS_IMG):
                filename_img = secure_filename(file_img.filename)
                file_img.save(os.path.join(app.config['UPLOAD_FOLDER_IMG'], filename_img))
                imagen = os.path.join(app.config['UPLOAD_FOLDER_IMG'], filename_img)
        
        # Manejo del PDF subido
        pdf = None
        if 'pdf' in request.files:
            file_pdf = request.files['pdf']
            if file_pdf and allowed_file(file_pdf.filename, ALLOWED_EXTENSIONS_PDF):
                filename_pdf = secure_filename(file_pdf.filename)
                file_pdf.save(os.path.join(app.config['UPLOAD_FOLDER_PDF'], filename_pdf))
                pdf = os.path.join(app.config['UPLOAD_FOLDER_PDF'], filename_pdf)
        
        # Actualizar la base de datos con los nuevos datos
        sql = "UPDATE libros SET titulo=%s, autor_id=%s, genero_id=%s, año_publicacion=%s, resenia=%s"
        val = [titulo, autor_id, genero_id, año_publicacion, resenia]
        
        if imagen:
            sql += ", imagen=%s"
            val.append(imagen)
        
        if pdf:
            sql += ", pdf=%s"
            val.append(pdf)
        
        sql += " WHERE libro_id=%s"
        val.append(libro_id)
        
        cursor.execute(sql, tuple(val))
        db.commit()
        
        flash('Libro editado correctamente.', 'success')
        return redirect(url_for('listar_libros'))
    
    # Obtener los datos actuales del libro para mostrar en el formulario
    cursor.execute("SELECT * FROM libros WHERE libro_id = %s", (libro_id,))
    libro = cursor.fetchone()
    
    cursor.execute("SELECT autor_id, CONCAT(nombre, ' ', apellidos) as nombre_completo FROM autores")
    autores = cursor.fetchall()
    cursor.execute("SELECT genero_id, nombre_genero FROM generos_literarios")
    generos = cursor.fetchall()
    
    return render_template('editar_libro.html', libro=libro, autores=autores, generos=generos)


# Ruta para eliminar libros
@app.route('/eliminar_libro/<int:libro_id>', methods=['POST'])
def eliminar_libro(libro_id):
    cursor.execute("DELETE FROM libros WHERE libro_id = %s", (libro_id,))
    db.commit()
    flash('Libro eliminado correctamente.', 'success')
    return redirect(url_for('listar_libros'))

# Ruta para agregar autores
@app.route('/agregar_autor', methods=['GET', 'POST'])
def agregar_autor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        nacionalidad = request.form['nacionalidad']
        
        sql = "INSERT INTO autores (nombre, apellidos, nacionalidad) VALUES (%s, %s, %s)"
        val = (nombre, apellidos, nacionalidad)
        cursor.execute(sql, val)
        db.commit()
        flash('Autor agregado correctamente.', 'success')
        return redirect(url_for('agregar_libro'))
    
    return render_template('agregar_autor.html')

# Clave secreta para sesiones
app.secret_key = 'ClaveSecretaDeAppSecretKey'

# Ruta para servir archivos PDF desde la carpeta 'static/Libros'
@app.route('/static/Libros/<pdf_filename>')
def ver_pdf(pdf_filename):
    return send_from_directory('static/Libros', pdf_filename)



# @app.route('/admin/usuarios')
# @role_required(['admin'])
# def listar_usuarios():
#     cursor.execute("SELECT u.id_usuario, u.nombre, u.apellido, u.username, u.email, r.nombre AS rol FROM usuarios u JOIN roles r ON u.rol_id = r.id")
#     usuarios = cursor.fetchall()
#     return render_template('listar_usuarios.html', usuarios=usuarios)

@app.route('/admin/usuarios')
@role_required(['admin'])
def listar_usuarios():
    # Realiza la consulta SQL para obtener todos los usuarios
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()  # Obtén todos los resultados como una lista de diccionarios o tuplas

    return render_template('listar_usuarios.html', usuarios=usuarios)



@app.route('/admin/agregar_usuario', methods=['GET', 'POST'])
@role_required(['admin'])
def agregar_usuario():
    if request.method == 'POST':
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
        rol_id = request.form['rol_id']

        # Convertir fechas a formatos correctos
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Encriptar la contraseña
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        sql = "INSERT INTO usuarios (nombre, apellido, username, email, fecha_nacimiento, fecha_registro, genero, pais, password, rol_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (nombre, apellido, username, email, fecha_nacimiento, fecha_registro, genero, pais, hashed_password, rol_id)
        cursor.execute(sql, val)
        db.commit()

        flash('Usuario agregado correctamente.', 'success')
        return redirect(url_for('listar_usuarios'))

    cursor.execute("SELECT id, nombre FROM roles")
    roles = cursor.fetchall()
    return render_template('agregar_usuario.html', roles=roles)

# Definir la ruta para editar un usuario específico
@app.route('/admin/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
@role_required(['admin'])  # Asegúrate de tener esta función decoradora definida para verificar los roles
def editar_usuario(user_id):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        fecha_nacimiento = request.form['fecha_nacimiento']
        genero = request.form['genero']
        pais = request.form['pais']
        rol_id = request.form['rol_id']

        # Convertir fecha de nacimiento al formato correcto si es necesario
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')

        # Actualizar los datos en la base de datos
        sql = "UPDATE usuarios SET nombre=%s, apellido=%s, email=%s, fecha_nacimiento=%s, genero=%s, pais=%s, rol_id=%s WHERE id_usuario=%s"
        val = (nombre, apellido, email, fecha_nacimiento, genero, pais, rol_id, user_id)
        cursor.execute(sql, val)
        db.commit()

        flash('Usuario editado correctamente.', 'success')
        return redirect(url_for('listar_usuarios'))

    # Obtener los datos del usuario y los roles para el formulario de edición
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    usuario = cursor.fetchone()  # Asegúrate de que cursor es un cursor de MySQL y usuario es un diccionario
    cursor.execute("SELECT id, nombre FROM roles")
    roles = cursor.fetchall()

    return render_template('editar_usuario.html', usuario=usuario, roles=roles)



@app.route('/admin/eliminar_usuario/<int:user_id>', methods=['POST'])
@role_required(['admin'])
def eliminar_usuario(user_id):
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (user_id,))
    db.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('listar_usuarios'))




if __name__ == '__main__':
    app.run(debug=True)

# Cierra la conexión con la base de datos al finalizar la aplicación
@app.teardown_appcontext
def close_db_connection(exception=None):
    db.close()

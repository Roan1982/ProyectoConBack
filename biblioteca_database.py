import pymysql

# Configuración de la conexión a la base de datos
db = pymysql.connect(host="localhost", user="root", password="root")
cursor = db.cursor()

# Sentencias SQL para crear la base de datos y las tablas
create_database_query = "CREATE DATABASE IF NOT EXISTS BIBLIOTECA"
use_database_query = "USE BIBLIOTECA"

# Sentencia SQL para crear la tabla autores
create_autores_table_query = """
    CREATE TABLE IF NOT EXISTS autores (
        autor_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        nacionalidad VARCHAR(50)
    )
"""

# Sentencia SQL para crear la tabla generos_literarios
create_generos_literarios_table_query = """
    CREATE TABLE IF NOT EXISTS generos_literarios (
        genero_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_genero VARCHAR(100) NOT NULL
    )
"""

# Sentencia SQL para crear la tabla de usuarios
create_usuarios_table_query = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        genero VARCHAR(20) NOT NULL,
        pais VARCHAR(100),
        password VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

# Sentencia SQL para crear la tabla libros
create_libros_table_query = """
CREATE TABLE IF NOT EXISTS libros (
    libro_id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor_id INT,
    genero_id INT,
    año_publicacion INT,
    imagen VARCHAR(255),  -- Campo para la ruta de la imagen
    resenia TEXT,         -- Campo para la reseña del libro
    pdf VARCHAR(255),     -- Campo para la ruta del archivo PDF
    FOREIGN KEY (autor_id) REFERENCES autores(autor_id),
    FOREIGN KEY (genero_id) REFERENCES generos_literarios(genero_id)
);
"""


# Sentencia SQL para crear la tabla opiniones
create_opiniones_table_query = """
    CREATE TABLE IF NOT EXISTS opiniones (
        opinion_id INT AUTO_INCREMENT PRIMARY KEY,
        libro_id INT,
        opinion_texto TEXT,
        puntaje INT,
        fecha_opinion DATE,
        FOREIGN KEY (libro_id) REFERENCES libros(libro_id)
    )
"""

try:
    # Crear la base de datos
    cursor.execute(create_database_query)
    print("Base de datos 'BIBLIOTECA' creada correctamente.")
    
    # Usar la base de datos 'BIBLIOTECA'
    cursor.execute(use_database_query)
    print("Usando la base de datos 'BIBLIOTECA'.")

    # Crear la tabla autores
    cursor.execute(create_autores_table_query)
    print("Tabla 'autores' creada correctamente.")
    
    # Crear la tabla generos_literarios
    cursor.execute(create_generos_literarios_table_query)
    print("Tabla 'generos_literarios' creada correctamente.")
    
    # Insertar géneros literarios de ejemplo
    insert_query = """
        INSERT INTO generos_literarios (nombre_genero) VALUES
        ('Ficción'),
        ('Fantasía'),
        ('Ciencia ficción'),
        ('Misterio'),
        ('Romance'),
        ('Aventura'),
        ('Terror'),
        ('Histórico'),
        ('Infantil'),
        ('Biografía'),
        ('Aventuras y Acción'),
        ('Cuentos infantiles'),
        ('Didáctica'),
        ('Fábulas y Leyendas'),
        ('Noches de Tormenta'),
        ('Audiolibros')
    """
    cursor.execute(insert_query)
    db.commit()
    print("Datos insertados correctamente en la tabla 'generos_literarios'.")
    
    # Crear la tabla usuarios
    cursor.execute(create_usuarios_table_query)
    print("Tabla 'usuarios' creada correctamente.")
    
    # Crear la tabla libros
    cursor.execute(create_libros_table_query)
    print("Tabla 'libros' creada correctamente.")
    
    # Crear la tabla opiniones
    cursor.execute(create_opiniones_table_query)
    print("Tabla 'opiniones' creada correctamente.")
    
    # Confirmar todos los cambios
    db.commit()

except pymysql.MySQLError as e:
    print(f"Error al ejecutar la consulta SQL: {e}")
    db.rollback()

finally:
    # Cerrar la conexión con la base de datos
    db.close()

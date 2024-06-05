from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Autor(db.Model):
    __tablename__ = 'autores'
    autor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    nacionalidad = db.Column(db.String(50))

class GeneroLiterario(db.Model):
    __tablename__ = 'Genero_literario'
    genero_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    usuario_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(45))
    email = db.Column(db.String(100), unique=True)
    fecha_nacimiento = db.Column(db.DateTime)
    fecha_registro = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(45))
    pais = db.Column(db.String(45))
    password = db.Column(db.String(255), nullable=False)

class Libro(db.Model):
    __tablename__ = 'libros'
    libro_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(25), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.autor_id'))
    genero_id = db.Column(db.Integer, db.ForeignKey('Genero_literario.genero_id'))
    año_publicacion = db.Column(db.Integer)

    autor = db.relationship('Autor', backref=db.backref('libros', lazy=True))
    genero = db.relationship('GeneroLiterario', backref=db.backref('libros', lazy=True))

class Opinion(db.Model):
    __tablename__ = 'opiniones'
    opinion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.libro_id'))
    opinion_texto = db.Column(db.Text)
    puntaje = db.Column(db.Integer)
    fecha_opinion = db.Column(db.Date)

    libro = db.relationship('Libro', backref=db.backref('opiniones', lazy=True))


    def __repr__(self):
        return f'<User {self.username}>'
    

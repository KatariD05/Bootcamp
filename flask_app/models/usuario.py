from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'[a-zA-Z]+$')
APELLIDO_REGEX = re.compile(r'[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.{8,})(?=.*[a-z])(?=.*[0-9]).*$')

DATABASE = 'esquema_eventos'

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        if len(resultado) > 0:
            return cls(resultado[0])
        else:
            return None

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        if len(resultado) > 0:
            return cls(resultado[0])
        else:
            return None
        
    @staticmethod
    def valid_login(data):
        is_valid = True
        if len(data['email']) <=0:
            flash('El campo de email no puede estar vacío', 'danger')
            is_valid = False
        if len(data['password']) <=0:
            flash('El campo de password no puede estar vacío', 'danger')
            is_valid = False
        return is_valid
        
    @staticmethod
    def valid_user(data):
        is_valid = True
        if (data['password'] != data['confirmpassword']):
            flash('La contraseña no coincide', 'danger')
            is_valid = False
        query = "select * from usuarios where email = %(email)s;"
        resultado_query = connectToMySQL(DATABASE).query_db(query, data)
        if len(resultado_query) > 0:
            flash('El email ya esta registrado', 'danger')
            is_valid = False
        if len(data['nombre']) <=0:
            flash('El campo de nombre no puede estar vacío', 'danger')
            is_valid = False
        if len(data['nombre']) < 2:
            flash('El nombre debe de tener más de 2 letras', 'danger')
            is_valid = False
        if len(data['apellido']) <=0:
            flash('El campo de apellido no puede estar vacío', 'danger')
            is_valid = False
        if len(data['apellido']) < 2:
            flash('El apellido debe de tener más de 2 letras', 'danger')
            is_valid = False
        if len(data['email']) <=0:
            flash('El campo de email no puede estar vacío', 'danger')
            is_valid = False
        if len(data['password']) <=0:
            flash('El campo de password no puede estar vacío', 'danger')
            is_valid = False
        if not NOMBRE_REGEX.match(data['nombre']):
            flash('El nombre no puede tener numeros o caracteres especiales', 'danger')
            is_valid = False
        if not APELLIDO_REGEX.match(data['apellido']):
            flash('El apellido no puede tener numeros o caracteres especiales', 'danger')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash('La contreseña no cumple con las caracteristicas minimas','danger')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('El email no cumple con el formato correcto','danger')
            is_valid = False
        return is_valid
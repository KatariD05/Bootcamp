from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import usuario
from flask import flash

DATABASE = 'esquema_eventos'

class Evento:
    def __init__(self, data):
        self.id = data['id']
        self.evento = data['evento']
        self.ubicacion = data['ubicacion']
        self.fecha = data['fecha']
        self.detalle = data['detalle']
        self.usuario_id = data['usuario_id']
        self.owner = None

    @classmethod
    def get_all_with_owner(cls):
        query = "SELECT * FROM eventos LEFT JOIN usuarios ON eventos.usuario_id = usuarios.id ORDER BY fecha asc;"
        resultados = connectToMySQL(DATABASE).query_db(query)
        eventos = []
        contador = 0
        for evento in resultados:
            eventos.append(cls(evento))
            data_usuario = {
                'id' : evento['usuarios.id'],
                'nombre' : evento['nombre'],
                'apellido' : evento['apellido'],
                'email' : evento['email'],
                'password' : evento['password'],
            }
            eventos[contador].owner = usuario.Usuario(data_usuario)
            contador +=1
        return eventos

    @classmethod
    def save_evento(cls, data):
        query = "INSERT INTO eventos (evento, ubicacion, fecha, detalle, usuario_id) VALUES (%(evento)s, %(ubicacion)s, %(fecha)s, %(detalle)s, %(usuario_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM eventos WHERE id = %(id)s;"
        resultados = connectToMySQL(DATABASE).query_db(query, data)
        if resultados:
            return resultados[0]
        return None
    
    @classmethod
    def update(cls, data):
        query = "UPDATE eventos SET evento = %(evento)s, ubicacion = %(ubicacion)s, fecha = %(fecha)s, detalle = %(detalle)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM eventos WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def valid_evento(data):
        is_valid = True
        if len(data['evento']) <=0:
            flash('El campo de evento no puede estar vacío', 'danger')
            is_valid = False
        if len(data['evento']) < 3:
            flash('Evento debe de tener más de 3 letras', 'danger')
            is_valid = False
        if len(data['ubicacion']) <=0:
            flash('El campo de ubicacion no puede estar vacío', 'danger')
            is_valid = False
        if len(data['ubicacion']) < 3:
            flash('Ubicacion debe de tener más de 3 letras', 'danger')
            is_valid = False
        if len(data['fecha']) <=0:
            flash('El campo de fecha no puede estar vacío', 'danger')
            is_valid = False
        if len(data['detalle']) <=0:
            flash('El campo de detalle no puede estar vacío', 'danger')
            is_valid = False
        if len(data['detalle']) < 3:
            flash('Detalle debe de tener más de 3 letras', 'danger')
            is_valid = False
        return is_valid
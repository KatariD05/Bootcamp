from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models.evento import Evento
from flask_app.models.usuario import Usuario
from flask import flash

@app.route('/eventos')
def mostrar_eventos():
    if session.get('usuario_id') == None:
        return redirect('/')
    eventos = Evento.get_all_with_owner()
    print(eventos)
    return render_template('eventos.html', eventos=eventos)

@app.route('/evento_nuevo')
def evento_nuevo():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para crear un evento.')
        return redirect('/inicio_sesion')
    return render_template('crear_evento.html')

@app.route('/crear_evento', methods=['POST'])
def crear_evento():
    data = {
        'usuario_id' : session['usuario_id'],
        'evento' : request.form['evento'],
        'ubicacion' : request.form['ubicacion'],
        'fecha' : request.form['fecha'],
        'detalle' : request.form['detalle']
    }
    if not Evento.valid_evento(data):
        return redirect('/evento_nuevo')
    Evento.save_evento(data)
    return redirect('/eventos')

@app.route('/evento/ver/<int:id>')
def ver_evento(id):
    evento = Evento.get_by_id({'id': id})
    usuario_id = evento['usuario_id']
    usuario = Usuario.get_by_id({'id': usuario_id})
    return render_template("ver_evento.html", evento=evento, usuario=usuario)

@app.route('/evento/editar/<int:id>', methods=['GET'])
def editar_evento(id):
    evento = Evento.get_by_id({'id': id})
    return render_template("editar_evento.html", evento=evento)

@app.route('/evento/actualizar/<int:id>', methods=['POST'])
def actualizar_evento(id):
    data = {
        'evento' : request.form['evento'],
        'ubicacion' : request.form['ubicacion'],
        'fecha' : request.form['fecha'],
        'detalle' : request.form['detalle'],
        'id' : id
    }
    if not Evento.valid_evento(data):
        return redirect(url_for('editar_evento', id=id))
    Evento.update(data)
    return redirect('/eventos')

@app.route('/evento/eliminar/<int:id>')
def delete(id):
    Evento.delete({'id': id})
    flash('Evento eliminado exitosamente.')
    return redirect('/eventos')
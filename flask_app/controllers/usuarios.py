from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def nuevo_registro():
    data = {
        'nombre' : request.form['nombre'],
        'apellido' : request.form['apellido'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirmpassword' : request.form['confirmpassword']
    }
    if not Usuario.valid_user(data):
        return redirect('/')
    data['password'] = bcrypt.generate_password_hash(data['password'])
    data = {
        'id' : Usuario.save(data)
    }
    usuario = Usuario.get_by_id(data)
    if usuario is None:
        return redirect('/')
    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    session['apellido'] = usuario.apellido
    session['email'] = usuario.email
    return redirect('/eventos')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password'],
    }
    if not Usuario.valid_login(data):
        return redirect('/')
    usuario = Usuario.get_by_email(data)
    if not bcrypt.check_password_hash(usuario.password, data['password']):
        flash('Los datos ingresados no son validos', 'danger')
        return redirect('/')
    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    session['apellido'] = usuario.apellido
    session['email'] = usuario.email
    print(usuario.id)
    return redirect('/eventos')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
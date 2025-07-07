from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from ext import db, migrate
from werkzeug.security import generate_password_hash, check_password_hash # PARA PROTEGER LAS CONTRASEÑAS A FUTURO
import os
from modelos import Medico, Paciente, Cita, Diagnostico, Rol
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database", "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/medicos')
def medicos():
    return render_template('medicos.html')

@app.route('/registrar-medico', methods=['POST'])
def registrar_medico():
    # Validar los datos del formulario, que no tengan campos vacíos y que cumplan con los requisitos
    primer_nombre = request.form.get('primer_nombre')
    segundo_nombre = request.form.get('segundo_nombre')
    primer_apellido = request.form.get('primer_apellido')
    segundo_apellido = request.form.get('segundo_apellido')
    correo = request.form.get('correo')
    rfc = request.form.get('rfc')
    cedula_profesional = request.form.get('cedula_profesional')
    rol = request.form.get('rol')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not primer_nombre or not primer_apellido or not correo or not rfc or not cedula_profesional or not rol or not password or not confirm_password:
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('medicos'))
    if not rfc or len(rfc) != 13:
        flash('El RFC debe tener exactamente 13 caracteres.', 'error')
        return redirect(url_for('medicos'))
    if not cedula_profesional or len(cedula_profesional) < 5:
        flash('La cédula profesional debe tener al menos 5 caracteres.', 'error')
        return redirect(url_for('medicos'))
    if password != confirm_password:
        flash('Las contraseñas no coinciden.', 'error')
        return redirect(url_for('medicos'))
    else:
        try:
            rol = int(rol)  
            nuevo_medico = Medico(
                primer_nombre=primer_nombre,
                segundo_nombre=segundo_nombre,
                primer_apellido=primer_apellido,
                segundo_apellido=segundo_apellido,
                correo=correo,
                rfc=rfc,
                cedula_profesional=cedula_profesional,
                id_rol=rol,
                password=password,  # Aqui se debe usar generate_password_hash si se quiere proteger la contraseña, despues lo haremos
                # password=generate_password_hash(password, method='sha256')  # se ve algo asi
            )
            db.session.add(nuevo_medico)
            db.session.commit()
            print(f"Médico registrado: {nuevo_medico.primer_nombre} {nuevo_medico.primer_apellido}")
            flash('Médico registrado exitosamente.', 'success')
            return redirect(url_for('medicos'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar médico: {e}")
            flash('Error al registrar médico.', 'error')
            return redirect(url_for('medicos'))


@app.route('/pacientes')
def pacientes():
    return render_template('pacientes.html')

if __name__ == '__main__':
    app.run(port=4000, debug=True)
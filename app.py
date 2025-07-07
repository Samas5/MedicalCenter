from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash # PARA PROTEGER LAS CONTRASEÑAS A FUTURO
import os
from modelos import Medico, Paciente, Cita, Diagnostico, Rol
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database", "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/medicos')
def medicos():
    return render_template('medicos.html')

@app.route('/pacientes')
def pacientes():
    return render_template('pacientes.html')

if __name__ == '__main__':
    app.run(port=4000, debug=True)
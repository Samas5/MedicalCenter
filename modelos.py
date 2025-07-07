from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Medico(db.Model):
    __tablename__ = 'medicos'
    id = db.Column(db.Integer, primary_key=True)
    rfc = db.Column(db.String(15), unique=True, nullable=False) 
    primer_nombre = db.Column(db.String(50), nullable=False)
    segundo_nombre = db.Column(db.String(50))
    primer_apellido = db.Column(db.String(50), nullable=False)
    segundo_apellido = db.Column(db.String(50))
    cedula_profesional = db.Column(db.String(20), unique=True, nullable=False)
    correo = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id') ,nullable=False)
    estado = db.Column(db.Boolean, default=True)
    citas = db.relationship('Cita', backref='medico')
    pacientes = db.relationship('Paciente', secondary='medico_paciente', back_populates='medicos')

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    primer_nombre = db.Column(db.String(50), nullable=False)
    segundo_nombre = db.Column(db.String(50))
    primer_apellido = db.Column(db.String(50), nullable=False)
    segundo_apellido = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    enfermedades_cronicas = db.Column(db.String(200))
    alergias = db.Column(db.String(200))
    antecedentes_familiares = db.Column(db.String(200))
    estado = db.Column(db.Boolean, default=True)
    medicos = db.relationship('Medico', secondary='medico_paciente', back_populates='pacientes')
    
    citas = db.relationship('Cita', backref='paciente')

# Relación Medico_Paciente
medico_paciente = db.Table('medico_paciente',
    db.Column('id_medico', db.Integer, db.ForeignKey('medicos.id'), primary_key=True),
    db.Column('id_paciente', db.Integer, db.ForeignKey('pacientes.id'), primary_key=True)
)

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    medicos = db.relationship('Medico', backref='rol')
 
class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    id_medico = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    latidos_por_minuto = db.Column(db.Integer, nullable=False)
    saturacion_oxigeno = db.Column(db.Float, nullable=False)
    glucosa = db.Column(db.Float, nullable=False)
    estado = db.Column(db.Boolean, default=True)

    diagnostico = db.relationship('Diagnostico', backref='cita', uselist=False) # investigar uselist

class Diagnostico(db.Model):
    __tablename__ = 'diagnosticos'
    id = db.Column(db.Integer, primary_key=True)
    id_cita = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False)
    sintomas = db.Column(db.String(200))
    diagnostico = db.Column(db.String(200))
    tratamiento = db.Column(db.String(200))
    estudios_solicitados = db.Column(db.String(200))


from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo para Tickets
class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    asunto = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.Enum('Baja', 'Media', 'Alta'), nullable=False)
    estado = db.Column(db.Enum('Abierto', 'En proceso', 'Cerrado'), default='Abierto')
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())

    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    usuario = db.relationship('User', foreign_keys=[usuario_id], backref='tickets_creados')
    tecnico = db.relationship('User', foreign_keys=[tecnico_id], backref='tickets_asignados')

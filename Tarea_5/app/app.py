from flask import Flask, request
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, UserNeed
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------------------------
# Configuración del Proyecto
# ---------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
Principal(app)

# ---------------------------
# Base de Datos con SQLAlchemy puro
# ---------------------------
engine = create_engine('sqlite:///mi_base_de_datos.db')
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String)
    role = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Agregar usuario de ejemplo si no existe
if not session.query(Usuario).filter_by(email='juan.perez@example.com').first():
    nuevo_usuario = Usuario(nombre='Juan Pérez', email='juan.perez@example.com', role='admin')
    session.add(nuevo_usuario)
    session.commit()

# ---------------------------
# Roles y Permisos
# ---------------------------
roles_permissions = {
    "admin": ["create", "read", "update", "delete"],
    "editor": ["read", "update"],
    "user": ["read"]
}

def check_permission(role, action):
    return action in roles_permissions.get(role, [])

# ---------------------------
# Flask-Principal (Roles y Acceso)
# ---------------------------
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))
user_permission = Permission(RoleNeed('user'))

@app.before_request
def cargar_identidad():
    user_email = request.args.get('user')
    if user_email:
        usuario = session.query(Usuario).filter_by(email=user_email).first()
        if usuario:
            identidad = Identity(usuario.id)
            identidad.provides.add(UserNeed(usuario.id))
            identidad.provides.add(RoleNeed(usuario.role))
            identity_changed.send(app, identity=identidad)

@identity_loaded.connect_via(app)
def cuando_identidad_cargada(sender, identity):
    usuario = session.query(Usuario).filter_by(id=identity.id).first()
    if usuario:
        identity.provides.add(UserNeed(usuario.id))
        identity.provides.add(RoleNeed(usuario.role))

# ---------------------------
# Rutas protegidas
# ---------------------------

@app.route('/')
def inicio():
    return "Bienvenido a la aplicación con roles y permisos."

@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin():
    return "Panel del administrador"

@app.route('/edit')
def editar():
    user_email = request.args.get('user')
    usuario = session.query(Usuario).filter_by(email=user_email).first()
    if usuario and check_permission(usuario.role, 'update'):
        return "Página de edición"
    return "Acceso denegado", 403

@app.route('/read')
def leer():
    user_email = request.args.get('user')
    usuario = session.query(Usuario).filter_by(email=user_email).first()
    if usuario and check_permission(usuario.role, 'read'):
        return f"{usuario.nombre} puede leer esta página."
    return "Acceso denegado", 403

@app.route('/delete')
def eliminar():
    user_email = request.args.get('user')
    usuario = session.query(Usuario).filter_by(email=user_email).first()
    if usuario and check_permission(usuario.role, 'delete'):
        return "Página de eliminación"
    return "Acceso denegado", 403

# ---------------------------
# Ejecutar la App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)

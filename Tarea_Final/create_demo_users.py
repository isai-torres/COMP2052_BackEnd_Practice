from app import create_app, db
from app.models import Role, User

app = create_app()

with app.app_context():
    roles = ['Admin', 'Usuario', 'Técnico']
    for name in roles:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))

    db.session.commit()

    users = [
        {"username": "admin", "email": "admin@example.com", "password": "admin123", "role": "Admin"},
        {"username": "tecnico", "email": "tech@example.com", "password": "tech123", "role": "Técnico"},
        {"username": "usuario", "email": "user@example.com", "password": "user123", "role": "Usuario"}
    ]

    for u in users:
        if not User.query.filter_by(email=u["email"]).first():
            role = Role.query.filter_by(name=u["role"]).first()
            user = User(username=u["username"], email=u["email"], role=role)
            user.set_password(u["password"])
            db.session.add(user)

    db.session.commit()
    print("Usuarios de prueba creados.")

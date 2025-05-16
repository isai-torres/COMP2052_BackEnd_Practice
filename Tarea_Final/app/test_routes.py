from flask import Blueprint, jsonify
from app.models import Ticket

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def index():
    return '<h1>Sistema de Tickets - Prueba Activa</h1>'

@main.route('/api/tickets')
def api_tickets():
    tickets = Ticket.query.all()
    return jsonify([
        {
            "id": t.id,
            "asunto": t.asunto,
            "prioridad": t.prioridad,
            "estado": t.estado
        } for t in tickets
    ])

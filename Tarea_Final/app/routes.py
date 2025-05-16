from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import TicketForm, EstadoTicketForm, ChangePasswordForm
from app.models import db, Ticket, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name == 'Admin':
        tickets = Ticket.query.all()
    elif current_user.role.name == 'Técnico':
        tickets = Ticket.query.filter_by(tecnico_id=current_user.id).all()
    else:
        tickets = Ticket.query.filter_by(usuario_id=current_user.id).all()

    return render_template('dashboard.html', tickets=tickets)

@main.route('/tickets/nuevo', methods=['GET', 'POST'])
@login_required
def crear_ticket():
    form = TicketForm()
    form.tecnico_id.choices = [(t.id, t.username) for t in User.query.join(User.role).filter_by(name='Técnico').all()]
    form.tecnico_id.choices.insert(0, (0, 'No asignar'))

    if form.validate_on_submit():
        tecnico = form.tecnico_id.data if form.tecnico_id.data != 0 else None
        ticket = Ticket(
            asunto=form.asunto.data,
            descripcion=form.descripcion.data,
            prioridad=form.prioridad.data,
            usuario_id=current_user.id,
            tecnico_id=tecnico
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket creado correctamente.")
        return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form)

@main.route('/tickets/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    if current_user.id != ticket.usuario_id and current_user.role.name != 'Admin':
        flash("No tienes permiso para editar este ticket.")
        return redirect(url_for('main.dashboard'))

    form = TicketForm(obj=ticket)
    form.tecnico_id.choices = [(t.id, t.username) for t in User.query.join(User.role).filter_by(name='Técnico').all()]
    form.tecnico_id.choices.insert(0, (0, 'No asignar'))

    if form.validate_on_submit():
        ticket.asunto = form.asunto.data
        ticket.descripcion = form.descripcion.data
        ticket.prioridad = form.prioridad.data
        ticket.tecnico_id = form.tecnico_id.data if form.tecnico_id.data != 0 else None
        db.session.commit()
        flash("Ticket actualizado.")
        return redirect(url_for('main.dashboard'))

    return render_template('ticket_form.html', form=form, editar=True)

@main.route('/tickets/<int:id>/estado', methods=['GET', 'POST'])
@login_required
def cambiar_estado(id):
    ticket = Ticket.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Técnico'] or \
       (current_user.role.name == 'Técnico' and ticket.tecnico_id != current_user.id):
        flash("No tienes permiso para cambiar el estado.")
        return redirect(url_for('main.dashboard'))

    form = EstadoTicketForm(obj=ticket)

    if form.validate_on_submit():
        ticket.estado = form.estado.data
        db.session.commit()
        flash("Estado actualizado.")
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_estado.html', form=form, ticket=ticket)

@main.route('/tickets/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    if current_user.role.name != 'Admin':
        flash("Solo los administradores pueden eliminar tickets.")
        return redirect(url_for('main.dashboard'))

    db.session.delete(ticket)
    db.session.commit()
    flash("Ticket eliminado.")
    return redirect(url_for('main.dashboard'))

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('La contraseña actual es incorrecta.')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Contraseña actualizada correctamente.')
            return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("No tienes permiso para ver esta página.")
        return redirect(url_for('main.dashboard'))

    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)

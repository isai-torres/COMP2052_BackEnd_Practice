from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Usuario', 'Usuario'), ('Técnico', 'Técnico')], validators=[DataRequired()])
    submit = SubmitField('Register')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

class TicketForm(FlaskForm):
    asunto = StringField('Asunto', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    prioridad = SelectField('Prioridad', choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta')], validators=[DataRequired()])
    tecnico_id = SelectField('Asignar Técnico', coerce=int, validators=[Optional()])
    submit = SubmitField('Guardar')

class EstadoTicketForm(FlaskForm):
    estado = SelectField('Estado', choices=[('Abierto', 'Abierto'), ('En proceso', 'En proceso'), ('Cerrado', 'Cerrado')], validators=[DataRequired()])
    submit = SubmitField('Actualizar Estado')

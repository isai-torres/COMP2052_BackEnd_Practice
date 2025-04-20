# Import necessary classes and functions from Flask and Flask-WTF
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = "mi_clave_secreta" # This is required for CSRF protection

class LoginForm(FlaskForm):
  username = StringField("Nombre de Usuario", validators=[DataRequired(), Length(min=3)])
  password = PasswordField("Contraseña", validators=[DataRequired()])
  submit = SubmitField("Iniciar Sesión")

@app.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm() # Create an instance of the form

  # If the form is submitted and passes all validations
  if form.validate_on_submit():
    return f"Usuario: {form.username.data}"
  return render_template("login.html", form=form)

#----------------------------------------------------------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
# Define una ruta en Flask accesible en la URL /register.
# Acepta tanto GET (mostrar formulario) como POST (procesar formulario).
def register():
  error = None  # Inicializa la variable de error en None (sin error al inicio)

  if request.method == "POST": # Si el usuario envía el formulario (POST)
    username = request.form.get("username") # Obtiene el valor del campo 'username' enviado por el formulario HTML
    
    if not username: # Si no se ingresó ningún nombre de usuario
      error = "El nombre de usuario es obligatorio."
    else:
      return f"Usuario registrado: {username}" # Si el nombre de usuario fue ingresado correctamente
      # Retorna un mensaje de éxito (solo para pruebas, en la práctica se redirige)
  return render_template("register.html", error=error) # Si es GET o hubo un error, renderiza el formulario y muestra el error si existe


if __name__ == "__main__":
  app.run(debug=True)
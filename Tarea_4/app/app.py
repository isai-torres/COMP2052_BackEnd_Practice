from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = "clave"

class LoginForm(FlaskForm):
  email = StringField("Correo Electrónico:", validators = [DataRequired(), Email()])
  username = StringField("Nombre:", validators = [DataRequired(), Length(min = 3)])
  password = PasswordField("Contraseña:", validators = [DataRequired(), Length(min = 6)])
  submit = SubmitField("Iniciar Sesión")



@app.route("/login", methods = ["GET", "POST"])
def login():

  form = LoginForm()

  if form.validate_on_submit():
    return f"Usuario: {form.username.data}"
  
  return render_template("login.html", form = form)

@app.route("/register", methods = ["GET", "POST"])
def register():

  error = None

  if request.method == "POST":
    username = request.form.get("username")
    if not username:
      error = "El nombre de usuario es obligatorio."
    else:
      return f"Usuario registrado: {username}"
    
  return render_template("register.html", error = error)

if __name__ == "__main__":
  app.run(debug=True)
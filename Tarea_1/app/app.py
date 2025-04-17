from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def saludo():

  saludo = "Bienvenido a mi aplicación Flask para la clase de COMP 2052"

  return render_template("index.html", saludo = saludo)

@app.route("/bienvenido", methods=["GET"])
def bienvenido():
  return "Hola soy Isai Torres, Bienvenido a mi aplicación Flask para la clase de COMP 2052"

@app.route("/estudiante", methods=["POST"])

def estudiante():
  data = request.json
  nombre = data.get("nombre")
  return f"Hola, {nombre}!"

if __name__ == "__main__":
  app.run(debug = True)
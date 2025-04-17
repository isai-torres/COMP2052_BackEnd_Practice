from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/info", methods = ["GET"])
def info():
  estudiante = {
    "recinto" : "Inter de Arecibo",
    "nombre" : "John Doe",
    "correo" : "inter@edu"
  }
  return jsonify(estudiante)

@app.route("/crearEstudiante", methods = ["POST"])
def crearEstudiante():
  estudiante = request.json
  if "nombre" not in estudiante:
    return "Error nombre del estudiante no fue creado"
  
  elif "correo" not in estudiante:
    return "Error correo del estudiante no fue creado"
    
  return jsonify({"Mensaje" : "Nuevo Estudiante Creado", "data" : estudiante})

@app.route("/usuarios", methods = ["GET"])
def usuarios():
  estudiantes = ["Juan", "Pedro", "Maria", "Lopez"]
  return jsonify({"Estudiantes": estudiantes}), 200

if __name__ == "__main__":
  app.run(debug = True)
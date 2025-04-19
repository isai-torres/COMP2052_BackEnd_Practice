from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/saludo", methods = ["POST"])
def saludo():
  data = request.json
  nombre = data.get("nombre", "usuario")
  return jsonify({"mensaje" : f"Hola {nombre}"})

@app.route("/usuario", methods = ["POST"])
def usuario():
  data = request.json
  if not data or "nombre" not in data:
    return jsonify({"error" : "Datos incompletos"}), 400
  return jsonify({"mensaje" : "Usuario creado exitosamente"})

if __name__ == "__main__":
  app.run(debug = True)
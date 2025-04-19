from flask import Flask, render_template

app = Flask(__name__)

@app.route("/capstone")
def capstone():
    data = {
        "title": "Proyecto Capstone",
        "description": "Lista de Tareas:",
        "items": ["Diseñar la base de datos", "Crear API REST", "Conectar Front-End"]
    }
    return render_template("capstone.html", **data)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def capstone():
  data = {
    "title": "COMP 2052 - Tarea 3",
    "description": "Pagina Principal: Frontend y Backend Tarea 3",
    "requisitos": [
      "Saber Python",
      "Tener conocimientos básicos de API",
      "Conectar el Front-End con el Back-End",
      "Conocer el framework Flask"
    ]
  }
  return render_template("index.html", **data)

@app.route("/secundaria")
def secundaria():
  pizza = {
    "title" : "Pagina Secundaria COMP 2052 - Tarea 3",
    "description" : "Describiendo lo que lleva un Pizza: ",
    "toppings" : [
      "Peperoni", 
      "Queso",
      "jamón",
      "Salsa"
    ]
  }
  return render_template("pizza.html", **pizza)

if __name__ == "__main__":
  app.run(debug=True)

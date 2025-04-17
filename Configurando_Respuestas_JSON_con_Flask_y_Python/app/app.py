from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/producto", methods = ["GET"])
def producto():
  data = {
    "producto" : "Laptop",
    "precio" : 1200.00,
    "disponible" : True
  }
  return jsonify(data)

if __name__ == "__main__":
  app.run(debug = True)
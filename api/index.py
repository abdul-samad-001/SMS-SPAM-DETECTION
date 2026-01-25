from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/", methods=["GET"])
def home():
    return "SMS Spam Detection API is live 🚀"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    message = data.get("message", "")
    vector = vectorizer.transform([message])
    prediction = model.predict(vector)[0]
    return jsonify({"spam": bool(prediction)})


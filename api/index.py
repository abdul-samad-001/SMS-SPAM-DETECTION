from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle

app = Flask(__name__, template_folder="templates")
CORS(app)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    vector = vectorizer.transform([message])

    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0]

    confidence = float(max(probability))  # highest probability

    return jsonify({
        "spam": bool(prediction),
        "confidence": round(confidence * 100, 2)
    })



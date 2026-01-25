from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__, template_folder="templates")

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
    return jsonify({"spam": bool(prediction)})

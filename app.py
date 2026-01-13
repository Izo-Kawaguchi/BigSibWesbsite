from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # allows your frontend JS to call the backend

analyzer = SentimentIntensityAnalyzer()

def analyze_sentence(sentence):
    scores = analyzer.polarity_scores(sentence)

    if scores["compound"] >= 0.05:
        label = "Positive"
    elif scores["compound"] <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "sentence": sentence,
        "scores": scores,
        "label": label
    }

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    sentences = re.split(r'(?<=[.!?])\s+', text)

    results = [analyze_sentence(s) for s in sentences]

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

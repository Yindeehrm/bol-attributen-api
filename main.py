
from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Alle gesplitste JSON-bestanden combineren
attributen = []

for i in range(1, 20):  # Pas dit aan op basis van het aantal bestanden
    filename = f"bol_attributen_deel{i}.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            attributen.extend(json.load(f))

@app.route('/zoek', methods=['GET'])
def zoek_attribuut():
    zoekterm = request.args.get('q', '').lower()
    multivalue = request.args.get('multivalue')

    if not zoekterm:
        return jsonify({"error": "Geef een zoekterm op met ?q=..."}), 400

    resultaten = [a for a in attributen if zoekterm in a.get('id', '').lower() or zoekterm in a.get('name', '').lower()]

    if multivalue == "true":
        resultaten = [r for r in resultaten if r.get('multiValue') is True]

    return jsonify(resultaten)

@app.route('/alles', methods=['GET'])
def alle_attributen():
    return jsonify(attributen)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

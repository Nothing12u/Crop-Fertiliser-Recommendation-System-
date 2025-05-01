from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for local testing

def recommend_crop_and_fertiliser(data):
    nitrogen = data.get('nitrogen', 0)
    phosphorus = data.get('phosphorus', 0)
    potassium = data.get('potassium', 0)
    ph = data.get('ph', 7)
    soilType = data.get('soilType', '').lower()

    if 6 <= ph <= 7.5:
        if soilType == "loamy" or soilType == "silty":
            crop = "Wheat"
        elif soilType == "sandy":
            crop = "Groundnut"
        elif soilType == "clay":
            crop = "Rice"
        elif soilType == "peaty":
            crop = "Barley"
        else:
            crop = "Maize"
    elif ph < 6:
        crop = "Rice"
    else:
        crop = "Sugarcane"

    recommendations = []
    if nitrogen < 50:
        recommendations.append("Apply Nitrogen-based fertiliser (e.g. Urea)")
    if phosphorus < 30:
        recommendations.append("Apply Phosphorus-based fertiliser (e.g. Single super phosphate)")
    if potassium < 40:
        recommendations.append("Apply Potassium-based fertiliser (e.g. Muriate of potash)")
    if not recommendations:
        recommendations.append("Soil nutrient levels appear adequate, minimal fertiliser needed.")

    return {"crop": crop, "fertilisers": recommendations}

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    result = recommend_crop_and_fertiliser(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
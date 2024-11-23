from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle  
import numpy as np
import os

app = Flask(__name__)
CORS(app)

model_path = "model.pkl" 
with open(model_path, "rb") as f:
    model = pickle.load(f)

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Customer Churn Prediction API!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json 
        print("Received Data:", data)

        Features = np.array([
            data['CreditScore'],
            0 if data['Gender'] == 'Male' else 1, 
            data['Age'],
            data['Tenure'],
            data['Balance'],
            data['NumOfProducts'],
            data['HasCrCard'],
            data['IsActiveMember'],
            data['EstimatedSalary'],
            1 if data['Geography'] == 'Germany' else 0, 
            1 if data['Geography'] == 'Spain' else 0    
        ]).reshape(1, -1)

        # Make prediction
        prediction = model.predict(Features)[0]

        return jsonify({"prediction": int(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = os.getenv("PORT", 5000)  
    app.run(host='0.0.0.0', port=port, debug=True)

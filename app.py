from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle  
import numpy as np


app = Flask(__name__)
CORS(app)

with open("model.pkl", "rb") as f:
     model = pickle.load(f)

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Customer Churn Prediction API!"

@app.route("/predict", methods=["POST"])


def predict():
    try:
        # Get JSON data from the request
        data = request.json
        
        # Extract and preprocess features
        Features = np.array([
            data['CreditScore'],
            data['Geography'],     
            0 if data['Gender'] == "Male" else 1,    
            data['Age'],
            data['Tenure'],
            data['Balance'],
            data['NumOfProducts'],
            data['HasCrCard'],
            data['IsActiveMember'],
            data['EstimatedSalary']
        ]).reshape(1, -1)
        
        # Perform prediction
        prediction = model.predict(Features)[0]

        # Return prediction as JSON
        return jsonify({"prediction": int(prediction)})
    
    except Exception as e:
        # Return error message in case of failure
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
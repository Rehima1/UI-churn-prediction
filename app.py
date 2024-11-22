from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle  
import numpy as np
import os

app = Flask(__name__)
CORS(app)


model_path = "C:\Users\Rehima\OneDrive\سطح المكتب\JS\model.pkl" 
with open(model_path, "rb") as f:
    model = pickle.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        
        # Handle Geography encoding (one-hot encoding)
        geography = data['Geography']
        geography_germany = 1 if geography == "Germany" else 0
        geography_spain = 1 if geography == "Spain" else 0
        # For other countries (like France), both will be 0
        geography_france = 1 if geography == "France" else 0

        # Handle Gender encoding (0 for Male, 1 for Female)
        gender = data['Gender']
        gender_male = 0 if gender == "Male" else 1  # Male: 0, Female: 1

        # Prepare the feature array (ensure it contains the correct order and number of features)
        features = np.array([
            data['CreditScore'],        # Numeric feature
            gender_male,               # Gender (encoded as 0 or 1)
            data['Age'],               # Numeric feature
            data['Tenure'],            # Numeric feature
            data['Balance'],           # Numeric feature
            data['NumOfProducts'],     # Numeric feature
            data['HasCrCard'],         # Binary feature (0 or 1)
            data['IsActiveMember'],    # Binary feature (0 or 1)
            data['EstimatedSalary'],   # Numeric feature
            geography_germany,         # One-hot encoded geography feature (Germany)
            geography_spain            # One-hot encoded geography feature (Spain)
        ]).reshape(1, -1)  # Reshape for model input (1 sample with multiple features)

        # Ensure features are numeric and pass them to the model
        prediction = model.predict(features)[0]

        return jsonify({"prediction": int(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
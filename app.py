from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle  
import numpy as np
import os

app = Flask(__name__)
CORS(app)


model_path = os.getenv("MODEL_PATH", "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json  
        print("Received Data:", data)  
        
        gender = 0 if data['Gender'] == 'Male' else 1

        geography_germany = 1 if data['Geography'] == 'Germany' else 0
        geography_spain = 1 if data['Geography'] == 'Spain' else 0

        Features = np.array([
            data['CreditScore'],
            gender,  
            data['Age'],
            data['Tenure'],
            data['Balance'],
            data['NumOfProducts'],
            data['HasCrCard'],
            data['IsActiveMember'],
            data['EstimatedSalary'],
            geography_germany, 
            geography_spain    
        ]).reshape(1, -1)

        prediction = model.predict(Features)[0]

        return jsonify({"prediction": int(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == "__main__":
    port = os.getenv("PORT", 5000)  
    app.run(host='0.0.0.0', port=5000, debug=True)
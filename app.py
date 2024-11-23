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

        required_fields = [
            'CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
            'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Geography', 'Gender'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

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
            1 if data['Geography'] == 'Spain' else 0,    
        ]).reshape(1, -1)  

        prediction = model.predict(Features)[0] 

        return jsonify({"prediction": int(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == "__main__":
    port = os.getenv("PORT", 5000)  
    app.run(host='0.0.0.0', port=5000, debug=True)
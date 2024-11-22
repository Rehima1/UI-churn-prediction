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

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Customer Churn Prediction API!"

def preprocess_geography(geography):
    if geography == "Germany":
        return [1, 0]
    elif geography == "Spain":
        return [0, 1]
    elif geography == "France":  
        return [0, 0]
    else:
        raise ValueError("Invalid Geography value")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print("Received Data:", data)  

        geography_encoded = preprocess_geography(data['Geography'])
        gender_encoded = 0 if data['Gender'] == "Male" else 1 

       
        Features = np.array([
            data['CreditScore'],     
            gender_encoded,          
            data['Age'],            
            data['Tenure'],          
            data['Balance'],         
            data['NumOfProducts'],   
            data['HasCrCard'],       
            data['IsActiveMember'],  
            data['EstimatedSalary'], 
            *geography_encoded       
        ]).reshape(1, -1)

        prediction = model.predict(Features)[0]

        return jsonify({"prediction": int(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = os.getenv("PORT", 5000)  
    app.run(host='0.0.0.0', port=5000, debug=True)
import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    CustomerId: "",
    CustomerName: "", 
    CreditScore: "",
    Geography: "",
    Gender: "",
    Age: "",
    Tenure: "",
    Balance: "",
    NumOfProducts: "",
    HasCrCard: "",
    IsActiveMember: "",
    EstimatedSalary: "",
  });

  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChanges = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setFormData({ ...formData, [name]: checked ? 1 : 0 });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const dataForModel = {
      CustomerIcod: formData.CustomerId,  
      CreditSre: formData.CreditScore,
      Geography: formData.Geography,
      Gender: formData.Gender,
      Age: formData.Age,
      Tenure: formData.Tenure,
      Balance: formData.Balance,
      NumOfProducts: formData.NumOfProducts,
      HasCrCard: formData.HasCrCard,
      IsActiveMember: formData.IsActiveMember,
      EstimatedSalary: formData.EstimatedSalary,
    };

    try {
      const response = await axios.post("https://flask-churn-prediction-3.onrender.com/predict", dataForModel); // Replace with your API URL
      setPrediction(response.data.prediction);
    } catch (err) {
      setError("Error predicting churn. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      CustomerId: "",
      CustomerName: "", 
      CreditScore: "",
      Geography: "",
      Gender: "",
      Age: "",
      Tenure: "",
      Balance: "",
      NumOfProducts: "",
      HasCrCard: 0,
      IsActiveMember: 0,
      EstimatedSalary: "",
    });
    setPrediction("");
    setError("");
  };

  return (
    <div className="App">
      <h1>Customer Churn Prediction</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Customer ID:
          <input
            type="text"
            name="CustomerId"
            value={formData.CustomerId}
            onChange={handleChanges}
            required
          />
        </label>

        <label>
          Customer Name: {/* New field for Customer Name */}
          <input
            type="text"
            name="CustomerName"
            value={formData.CustomerName}
            onChange={handleChanges}
            required
          />
        </label>

        <label>
          Credit Score:
          <input
            type="number"
            name="CreditScore"
            value={formData.CreditScore}
            onChange={handleChanges}
            required
          />
        </label>

        <label>
          Geography:
          <select
            name="Geography"
            value={formData.Geography}
            onChange={handleChanges}
            required
          >
            <option value="">Select</option>
            <option value="France">France</option>
            <option value="Germany">Germany</option>
            <option value="Spain">Spain</option>
          </select>
        </label>

        <label>
          Gender:
          <select
            name="Gender"
            value={formData.Gender}
            onChange={handleChanges}
            required
          >
            <option value="">Select</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </label>

        <label>
          Age:
          <input
            type="number"
            name="Age"
            value={formData.Age}
            onChange={handleChanges}
            required
          />
        </label>

        <label>
          Tenure:
          <input
            type="number"
            name="Tenure"
            value={formData.Tenure}
            onChange={handleChanges}
            required
          />
        </label>

        <label>
          Balance:
          <input
            type="number"
            name="Balance"
            value={formData.Balance}
            onChange={handleChanges}
            required
          />
        </label>

        <label>
          Number of Products:
          <input
            type="number"
            name="NumOfProducts"
            value={formData.NumOfProducts}
            onChange={handleChanges}
            required
          />
        </label>

        <label>
          Has Credit Card:
          <input
            type="checkbox"
            name="HasCrCard"
            checked={formData.HasCrCard === 1}
            onChange={handleCheckboxChange}
          />
        </label>

        <label>
          Is Active Member:
          <input
            type="checkbox"
            name="IsActiveMember"
            checked={formData.IsActiveMember === 1}
            onChange={handleCheckboxChange}
          />
        </label>

        <label>
          Estimated Salary:
          <input
            type="number"
            name="EstimatedSalary"
            value={formData.EstimatedSalary}
            onChange={handleChanges}
            required
          />
        </label>

        <div className="buttons">
          <button type="submit" disabled={loading}>
            {loading ? "Predicting..." : "Submit"}
          </button>
          <button type="button" onClick={handleReset}>
            Reset
          </button>
        </div>
      </form>

      {prediction && <div className="result">Prediction: {prediction}</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default App;


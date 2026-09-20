# 🛡️ FraudShield — End-to-End ML Fraud Detection System

> An end-to-end Machine Learning system for detecting potentially fraudulent financial transactions using XGBoost, FastAPI, and a cloud-deployed web application.

🌐 **Live Demo:** https://fraud-detection-system-dfji.onrender.com  
📂 **GitHub:** https://github.com/parth-godage/fraud-detection-system

---

## 🚀 Overview

Fraud detection is a highly imbalanced classification problem where fraudulent transactions represent only a very small percentage of all transactions.

**FraudShield** is an end-to-end Machine Learning project designed to identify potentially fraudulent transactions and expose the trained model through a real-time web application.

Instead of stopping at model training in a Jupyter Notebook, this project takes the complete journey:

```text
Data
  ↓
Exploratory Data Analysis
  ↓
Feature Selection
  ↓
Preprocessing
  ↓
Class Imbalance Handling
  ↓
XGBoost Model
  ↓
Threshold Optimization
  ↓
Model Evaluation
  ↓
FastAPI REST API
  ↓
Interactive Web Interface
  ↓
Cloud Deployment

🎯 Problem Statement

Financial fraud detection is challenging because fraudulent transactions are extremely rare compared to legitimate transactions.

The PaySim dataset used in this project contains:

6.36M+ transactions
8,213 fraudulent transactions
6.35M+ legitimate transactions
Fraud rate of approximately 0.13%

A model that predicts every transaction as legitimate could achieve very high accuracy while completely failing to detect fraud.

Therefore, this project focuses on handling class imbalance and evaluating the model using fraud-focused metrics such as Precision, Recall, F1-score, and ROC-AUC.

💡 Solution

FraudShield uses an XGBoost classifier to identify potentially fraudulent transactions.

The system:

Processes transaction information
Encodes categorical transaction types
Handles severe class imbalance using weighted learning
Generates a fraud probability
Optimizes the classification threshold using validation data
Exposes the trained model through a FastAPI REST API
Provides an interactive web interface
Deploys the complete application to the cloud
📊 Dataset

This project uses the PaySim synthetic financial transaction dataset.

Dataset Statistics
Property	Value
Total Transactions	6,362,620
Fraudulent Transactions	8,213
Legitimate Transactions	6,354,407
Fraud Rate	~0.13%
Transaction Types	5
Transaction Types
PAYMENT
TRANSFER
CASH_OUT
CASH_IN
DEBIT
🧠 Features Used

The final model uses the following features:

step
type
amount
oldbalanceOrg
oldbalanceDest
Feature Description
Feature	Description
step	Simulated time step; each step represents one hour
type	Transaction type
amount	Transaction amount
oldbalanceOrg	Sender's previous balance
oldbalanceDest	Receiver's previous balance
⚙️ Machine Learning Pipeline
1. Train-Test Split

A stratified train-test split is used to preserve the minority fraud class distribution.

train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)
2. Class Imbalance Handling

The dataset is highly imbalanced.

The model uses XGBoost's:

scale_pos_weight

to give greater importance to fraudulent transactions during training.

3. Categorical Encoding

The type feature is encoded using:

OneHotEncoder(handle_unknown="ignore")

The preprocessing and model are combined into a single Scikit-learn pipeline.

🌳 Model
XGBoost Classifier

XGBoost was selected because it performs strongly on structured/tabular datasets and supports:

Non-linear relationships
Class weighting
Probability prediction
Efficient training
Feature interactions
🎯 Threshold Optimization

For highly imbalanced fraud detection, a default classification threshold of 0.5 is not always suitable.

Instead, the classification threshold was optimized on validation data using F1-score.

Tuned Threshold
0.9891

The decision logic is:

Fraud Probability >= 0.9891
              ↓
            FRAUD

Fraud Probability < 0.9891
              ↓
         LEGITIMATE

This separates the model's probability score from the final classification decision.

📈 Model Performance

Evaluation was performed on a held-out test set.

Metric	Score
ROC-AUC	~0.9994
Fraud Precision	~90%
Fraud Recall	~81%
Fraud F1-Score	~85%
Confusion Matrix
                    Predicted
                  Legit    Fraud

Actual Legit    1,270,734    147
Actual Fraud          314   1,329

The model successfully identifies a large proportion of fraudulent transactions while keeping false fraud alerts relatively low on this test setup.

🏗️ System Architecture
                    ┌──────────────────────┐
                    │        User          │
                    │     Web Browser      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FraudShield UI    │
                    │    HTML/CSS/JS       │
                    └──────────┬───────────┘
                               │
                         POST /predict
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │      REST API        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Pydantic Validation│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   XGBoost Pipeline   │
                    │ Preprocessing + Model│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Fraud Probability   │
                    └──────────┬───────────┘
                               │
                         Threshold 0.9891
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
             🚨 FRAUD                ✅ LEGITIMATE
🌐 REST API

FraudShield exposes the trained model through a FastAPI REST API.

Health Check
GET /health

Example response:

{
  "status": "healthy",
  "model": "PaySim XGBoost",
  "threshold": 0.9891
}
Fraud Prediction
POST /predict
Request
{
  "step": 1,
  "type": "TRANSFER",
  "amount": 1000000,
  "oldbalanceOrg": 1000000,
  "oldbalanceDest": 0
}
Response
{
  "prediction": 1,
  "result": "Fraud",
  "fraud_probability": 1.0,
  "threshold": 0.9891
}
📚 Interactive API Documentation

FastAPI automatically provides Swagger documentation.

Swagger UI

https://fraud-detection-system-dfji.onrender.com/docs

The API can be tested directly from the browser using the interactive Swagger interface.

🖥️ Web Application

FraudShield provides an interactive interface where users can enter:

Transaction Type
Transaction Amount
Transaction Step
Sender's Previous Balance
Receiver's Previous Balance

The system then generates:

Transaction
      ↓
Fraud Probability
      ↓
Risk Assessment
      ↓
Fraud / Legitimate
📁 Project Structure
fraud-detection-system/
│
├── app/
│   ├── main.py
│   │
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
│
├── models/
│   ├── fraud_paysim_pipeline.pkl
│   └── fraud_paysim_threshold.pkl
│
├── notebooks/
│   └── fraud_detection.ipynb
│
├── src/
│
├── data/
│   └── PaySim dataset
│
├── requirements.txt
├── .python-version
├── .gitignore
└── README.md
🛠️ Tech Stack
Machine Learning
Python
Pandas
NumPy
Scikit-learn
XGBoost
Backend
FastAPI
Pydantic
Uvicorn
Frontend
HTML5
CSS3
JavaScript
Deployment & Version Control
Git
GitHub
Render
💻 Run Locally
1. Clone the Repository
git clone https://github.com/parth-godage/fraud-detection-system.git
cd fraud-detection-system
2. Create Virtual Environment
Windows
python -m venv venv

Activate:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Start the FastAPI Server
uvicorn app.main:app --reload
5. Open the Application
http://127.0.0.1:8000
Swagger
http://127.0.0.1:8000/docs
Health Check
http://127.0.0.1:8000/health
☁️ Deployment

The application is deployed using Render.

Deployment workflow:

GitHub Repository
        ↓
Render
        ↓
Install Dependencies
        ↓
Start FastAPI
        ↓
Public HTTPS Application
Production Start Command
uvicorn app.main:app --host 0.0.0.0 --port $PORT
Live Application

🌐 https://fraud-detection-system-dfji.onrender.com

🔐 Production-Style Features

The application includes:

✅ Pydantic request validation
✅ Transaction type validation
✅ Input range validation
✅ Health check endpoint
✅ REST API
✅ Persistent ML model
✅ Cloud deployment
✅ Git-based version control
✅ Interactive Swagger API documentation
🎓 Key Learning Outcomes

This project helped me understand how to take a Machine Learning model beyond a Jupyter Notebook and turn it into an accessible application.

The complete workflow was:

Data
 ↓
EDA
 ↓
Feature Selection
 ↓
Preprocessing
 ↓
Class Imbalance Handling
 ↓
Model Training
 ↓
Model Evaluation
 ↓
Threshold Optimization
 ↓
Model Serialization
 ↓
FastAPI
 ↓
Frontend Integration
 ↓
GitHub
 ↓
Cloud Deployment
Key Takeaway

Machine Learning does not end when the model is trained. A useful ML system needs to be served, integrated, deployed, and made accessible to users.

⚠️ Limitations

This project uses the PaySim synthetic dataset.

Therefore:

The dataset does not represent real banking transactions.
Model performance on PaySim does not guarantee equivalent real-world performance.
Synthetic simulator patterns may make the classification problem easier than real-world fraud detection.
A real banking fraud detection system would require additional real-time behavioral, historical, and transactional signals.

This project is therefore intended as an end-to-end ML engineering and fraud detection prototype.

🚀 Future Improvements

Planned improvements include:

Docker containerization
GitHub Actions CI/CD
Model monitoring
Data drift detection
Explainable AI
Automated model retraining
Authentication and authorization
API rate limiting
Production logging
Real-world transaction data
Model versioning

Future architecture:

Current System
      ↓
Docker
      ↓
CI/CD
      ↓
Model Monitoring
      ↓
Data Drift Detection
      ↓
Explainable AI
      ↓
Automated Retraining
👨‍💻 Author
Parth Godage

Computer Engineering Student | Machine Learning | AI Engineering

🔗 GitHub:
https://github.com/parth-godage

🌐 Live Project:
https://fraud-detection-system-dfji.onrender.com

⭐ Project

If you find this project useful or interesting, feel free to explore the repository and try the live application.

Built with Python, Machine Learning, FastAPI, and a lot of debugging. 🚀

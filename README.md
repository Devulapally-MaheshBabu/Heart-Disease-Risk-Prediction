# CardioScan – Heart Disease Risk Predictor

A production-quality full-stack ML project built with React, FastAPI, and scikit-learn.

## 🏗️ Project Structure

```
heart-disease-predictor/
│
├── ml/                          # Machine Learning
│   ├── train_model.py           # Training script
│   ├── requirements.txt         # ML dependencies
│   ├── model.pkl                # Saved model (generated)
│   └── model_metadata.json      # Model metrics (generated)
│
├── backend/                     # FastAPI Backend
│   ├── main.py                  # API server
│   └── requirements.txt         # Backend dependencies
│
└── frontend/                    # React Frontend
    ├── src/
    │   ├── App.jsx              # Main component
    │   ├── App.css              # Styles
    │   ├── main.jsx             # Entry point
    │   └── index.css            # Global reset
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## 🗃️ Dataset

**UCI Cleveland Heart Disease Dataset**
- 303 patients, 13 clinical features
- Target: binary (0 = no disease, 1 = disease)
- Source: UCI Machine Learning Repository

**Features used:**
| Feature    | Description                           |
|------------|---------------------------------------|
| age        | Age in years                          |
| sex        | Sex (0=Female, 1=Male)               |
| cp         | Chest pain type (0–3)                |
| trestbps   | Resting blood pressure (mmHg)        |
| chol       | Serum cholesterol (mg/dl)            |
| fbs        | Fasting blood sugar >120 mg/dl       |
| restecg    | Resting ECG results (0–2)            |
| thalach    | Max heart rate achieved              |
| exang      | Exercise-induced angina              |
| oldpeak    | ST depression by exercise            |
| slope      | Slope of peak exercise ST segment    |
| ca         | # major vessels by fluoroscopy (0–3) |
| thal       | Thalassemia type                     |

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

---

### Step 1: Train the ML Model

```bash
cd ml
pip install -r requirements.txt
python train_model.py
```

This will:
- Download the UCI dataset automatically
- Preprocess, train, and evaluate the model
- Save `model.pkl` and `model_metadata.json`

Expected output:
```
Accuracy  : ~0.84
ROC-AUC   : ~0.91
CV Accuracy: ~0.82 ± 0.04
```

---

### Step 2: Start the FastAPI Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Visit: http://localhost:8000/docs  (Swagger UI auto-generated)

---

### Step 3: Start the React Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:5173

---

## 🔌 API Reference

### `POST /predict`

**Request Body:**
```json
{
  "age": 54,
  "sex": 1,
  "cp": 2,
  "trestbps": 130,
  "chol": 245,
  "fbs": 0,
  "restecg": 1,
  "thalach": 162,
  "exang": 0,
  "oldpeak": 0.0,
  "slope": 2,
  "ca": 0,
  "thal": 2
}
```

**Response:**
```json
{
  "prediction": 0,
  "label": "No Disease Detected",
  "probability": 0.18,
  "risk_level": "Low",
  "message": "Low risk indicators detected. Maintain a healthy lifestyle."
}
```

### Other Endpoints
- `GET /` — API status + model info
- `GET /health` — Health check
- `GET /model-info` — Full model metadata
- `GET /docs` — Swagger UI

---

## 🧪 Test with curl

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233,
    "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0,
    "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'
```

---

## 🚀 Two Ways to Scale This Project

### 1. Add a Database + Patient History
Use PostgreSQL + SQLAlchemy to store prediction history per patient. Add a `POST /patients` endpoint, let users track risk over time, and build a dashboard with trend charts. This turns a one-shot tool into a longitudinal monitoring system.

### 2. Replace Static Model with Online Learning / Model Registry
Integrate MLflow or BentoML to version your models. Build a retraining pipeline triggered by data drift (use Evidently AI). This adds CI/CD for ML — when new patient data comes in, the model can be retrained, evaluated, and hot-swapped without downtime.

---

## ⚕️ Disclaimer

This project is for educational purposes only. It does not constitute medical advice and should never be used for clinical decision-making.
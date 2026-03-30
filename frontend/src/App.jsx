import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "https://heart-disease-risk-prediction-w58h.onrender.com";
console.log("API_URL:", API_URL);

const FIELDS = [
  {
    key: "age",
    label: "Age",
    type: "number",
    min: 20,
    max: 100,
    step: 1,
    placeholder: "e.g. 54",
    hint: "Years (20–100)",
  },
  {
    key: "sex",
    label: "Sex",
    type: "select",
    options: [
      { value: 1, label: "Male" },
      { value: 0, label: "Female" },
    ],
  },
  {
    key: "cp",
    label: "Chest Pain Type",
    type: "select",
    options: [
      { value: 0, label: "0 – Typical Angina" },
      { value: 1, label: "1 – Atypical Angina" },
      { value: 2, label: "2 – Non-Anginal Pain" },
      { value: 3, label: "3 – Asymptomatic" },
    ],
  },
  {
    key: "trestbps",
    label: "Resting Blood Pressure",
    type: "number",
    min: 80,
    max: 220,
    step: 1,
    placeholder: "e.g. 130",
    hint: "mmHg",
  },
  {
    key: "chol",
    label: "Serum Cholesterol",
    type: "number",
    min: 100,
    max: 600,
    step: 1,
    placeholder: "e.g. 245",
    hint: "mg/dl",
  },
  {
    key: "fbs",
    label: "Fasting Blood Sugar >120 mg/dl",
    type: "select",
    options: [
      { value: 0, label: "No" },
      { value: 1, label: "Yes" },
    ],
  },
  {
    key: "restecg",
    label: "Resting ECG",
    type: "select",
    options: [
      { value: 0, label: "0 – Normal" },
      { value: 1, label: "1 – ST-T Wave Abnormality" },
      { value: 2, label: "2 – Left Ventricular Hypertrophy" },
    ],
  },
  {
    key: "thalach",
    label: "Max Heart Rate",
    type: "number",
    min: 60,
    max: 220,
    step: 1,
    placeholder: "e.g. 162",
    hint: "bpm",
  },
  {
    key: "exang",
    label: "Exercise-Induced Angina",
    type: "select",
    options: [
      { value: 0, label: "No" },
      { value: 1, label: "Yes" },
    ],
  },
  {
    key: "oldpeak",
    label: "ST Depression",
    type: "number",
    min: 0,
    max: 7,
    step: 0.1,
    placeholder: "e.g. 1.2",
    hint: "Exercise vs rest",
  },
  {
    key: "slope",
    label: "ST Slope",
    type: "select",
    options: [
      { value: 0, label: "0 – Upsloping" },
      { value: 1, label: "1 – Flat" },
      { value: 2, label: "2 – Downsloping" },
    ],
  },
  {
    key: "ca",
    label: "Major Vessels (Fluoroscopy)",
    type: "select",
    options: [
      { value: 0, label: "0" },
      { value: 1, label: "1" },
      { value: 2, label: "2" },
      { value: 3, label: "3" },
    ],
  },
  {
    key: "thal",
    label: "Thalassemia",
    type: "select",
    options: [
      { value: 0, label: "0 – Normal" },
      { value: 1, label: "1 – Fixed Defect" },
      { value: 2, label: "2 – Reversible Defect" },
      { value: 3, label: "3 – Unknown" },
    ],
  },
];

const DEFAULTS = {
  age: "",
  sex: 1,
  cp: 0,
  trestbps: "",
  chol: "",
  fbs: 0,
  restecg: 0,
  thalach: "",
  exang: 0,
  oldpeak: "",
  slope: 0,
  ca: 0,
  thal: 2,
};

const RISK_CONFIG = {
  Low: { color: "#22c55e", bg: "#f0fdf4", border: "#bbf7d0", icon: "✅" },
  Moderate: { color: "#f59e0b", bg: "#fffbeb", border: "#fde68a", icon: "⚠️" },
  High: { color: "#ef4444", bg: "#fef2f2", border: "#fecaca", icon: "🚨" },
};

export default function App() {
  const [form, setForm] = useState(DEFAULTS);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // Convert all values to floats
    const payload = Object.fromEntries(
      Object.entries(form).map(([k, v]) => [k, parseFloat(v)]),
    );

    try {
      const res = await axios.post(`${API_URL}/predict`, payload);
      setResult(res.data);
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        "Failed to connect to backend. Is it running?";
      setError(typeof msg === "string" ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setForm(DEFAULTS);
    setResult(null);
    setError(null);
  };

  const risk = result ? RISK_CONFIG[result.risk_level] : null;

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">♥</span>
            <div>
              <h1>CardioScan</h1>
              <p>Heart Disease Risk Predictor</p>
            </div>
          </div>
        </div>
      </header>

      <main className="main">

        <div className="card form-card">
          <h2 className="section-title">Patient Information</h2>
          <form onSubmit={handleSubmit}>
            <div className="grid">
              {FIELDS.map((field) => (
                <div className="field" key={field.key}>
                  <label htmlFor={field.key}>{field.label}</label>
                  {field.type === "select" ? (
                    <select
                      id={field.key}
                      value={form[field.key]}
                      onChange={(e) => handleChange(field.key, e.target.value)}
                    >
                      {field.options.map((opt) => (
                        <option key={opt.value} value={opt.value}>
                          {opt.label}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <div className="input-wrap">
                      <input
                        id={field.key}
                        type="number"
                        min={field.min}
                        max={field.max}
                        step={field.step}
                        placeholder={field.placeholder}
                        value={form[field.key]}
                        onChange={(e) =>
                          handleChange(field.key, e.target.value)
                        }
                        required
                      />
                      {field.hint && <span className="hint">{field.hint}</span>}
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="btn-row">
              <button
                type="button"
                className="btn btn-ghost"
                onClick={handleReset}
              >
                Reset
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner" /> Analyzing...
                  </>
                ) : (
                  <>
                    <span>♥</span> Predict Risk
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {error && (
          <div className="card error-card">
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && risk && (
          <div
            className="card result-card"
            style={{ borderColor: risk.border, background: risk.bg }}
          >
            <div className="result-header">
              <span className="result-icon">{risk.icon}</span>
              <div>
                <h2 className="result-label" style={{ color: risk.color }}>
                  {result.label}
                </h2>
                <span className="risk-badge" style={{ background: risk.color }}>
                  {result.risk_level} Risk
                </span>
              </div>
            </div>

            <p className="result-message">{result.message}</p>

            <div className="prob-bar-wrap">
              <div className="prob-label">
                <span>Disease Probability</span>
                <strong style={{ color: risk.color }}>
                  {(result.probability * 100).toFixed(1)}%
                </strong>
              </div>
              <div className="prob-bar-bg">
                <div
                  className="prob-bar-fill"
                  style={{
                    width: `${result.probability * 100}%`,
                    background: risk.color,
                  }}
                />
              </div>
            </div>

            <div className="meta-row">
              <div className="meta-item">
                <span>Prediction</span>
                <strong>
                  {result.prediction === 1 ? "Positive" : "Negative"}
                </strong>
              </div>
              <div className="meta-item">
                <span>Risk Level</span>
                <strong style={{ color: risk.color }}>
                  {result.risk_level}
                </strong>
              </div>
              <div className="meta-item">
                <span>Confidence</span>
                <strong>{(result.probability * 100).toFixed(1)}%</strong>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

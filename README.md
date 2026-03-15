# 🔐 AI Network Threat Detection Dashboard

## 🚀 Project Overview
An end-to-end Machine Learning solution for real-time network intrusion detection.

### 📸 Dashboard Screenshots

#### 1. Upload & Detection
![Upload Part](screenshots/upload_detection.png)

#### 2. Detection Results Table
![Results Table](screenshots/result_table.png)

#### 3. Overall Composition (Pie Chart)
![Pie Chart](screenshots/piechart.png)

#### 4. Threat History (Histogram)
![Histogram](screenshots/histogram.png)

---

## 🏆 Model Performance
The system uses a **Random Forest Classifier** achieving an overall accuracy of **99.92%**.

| Attack Class | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| **DoS** | 1.00 | 1.00 | 1.00 | 9,186 |
| **Normal** | 1.00 | 1.00 | 1.00 | 13,469 |
| **Probe** | 1.00 | 1.00 | 1.00 | 2,331 |
| **R2L** | 0.98 | 0.98 | 0.98 | 199 |
| **U2R** | 1.00 | 0.90 | 0.95 | 10 |

## 📊 Dataset Details: NSL-KDD
The model is trained on the industry-standard **NSL-KDD dataset**.
* **Preprocessing:** One-Hot Encoding and Standard Scaling.
* **Input Features:** 153 engineered features.
* **Target Classes:** DoS, Probe, R2L, U2R, and Normal.

## ⚙️ Installation & Setup

### 1. Set up Virtual Environment
`python -m venv venv`

### 2. Install Dependencies
`pip install -r requirements.txt`

### 3. Run the AI Engine
`uvicorn api.app:app --reload`

### 4. Run the Dashboard
`streamlit run dashboard.py`
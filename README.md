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

## ⚙️ Installation & Setup

### 1. Set up Virtual Environment
`python -m venv venv`

### 2. Install Dependencies
`pip install -r requirements.txt`

### 3. Run the AI Engine
`uvicorn api.app:app --reload`

### 4. Run the Dashboard
`streamlit run dashboard.py`
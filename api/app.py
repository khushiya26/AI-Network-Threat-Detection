import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI()

class InputData(BaseModel):
    data: list
original_columns = [
    'duration','protocol_type','service','flag','src_bytes','dst_bytes',
    'land','wrong_fragment','urgent','hot','num_failed_logins',
    'logged_in','num_compromised','root_shell','su_attempted',
    'num_root','num_file_creations','num_shells','num_access_files',
    'num_outbound_cmds','is_host_login','is_guest_login',
    'count','srv_count','serror_rate','srv_serror_rate','rerror_rate',
    'srv_rerror_rate','same_srv_rate','diff_srv_rate',
    'srv_diff_host_rate','dst_host_count','dst_host_srv_count',
    'dst_host_same_srv_rate','dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate','dst_host_srv_diff_host_rate',
    'dst_host_serror_rate','dst_host_srv_serror_rate',
    'dst_host_rerror_rate','dst_host_srv_rerror_rate'
]
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

model_path = os.path.join(BASE_DIR, "models", "threat_detection_model.pkl")
scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")
training_columns = joblib.load(os.path.join(BASE_DIR, "models", "feature_names.pkl"))

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)


attack_map = {
            0: "normal", 
            1: "dos", 
            2: "probe", 
            3: "r2l", 
            4: "u2r"
        }

@app.get("/")
def home():
    return {"message": "AI Network Threat Detection API"}

@app.post("/predict")
def predict(input_data: InputData):
    try:
        # 1. Load the entire batch at once
        df_input = pd.DataFrame(input_data.data, columns=original_columns)

        # 2. Batch Encoding and Alignment
        df_encoded = pd.get_dummies(df_input)
        df_final = df_encoded.reindex(columns=training_columns, fill_value=0)

        # 3. Batch Scaling and Prediction
        scaled_data = scaler.transform(df_final)
        predictions = model.predict(scaled_data)
        
        # 4. Map numeric results to lowercase labels
        inv_map = {0: "normal", 1: "dos", 2: "probe", 3: "r2l", 4: "u2r"}
        
        results = []
        for p in predictions:
            if isinstance(p, str):
                results.append(p.strip('.').lower())
            else:
                results.append(inv_map.get(p, "unknown"))

        return {"predictions": results}

    except Exception as e:
        return {"error": str(e)}
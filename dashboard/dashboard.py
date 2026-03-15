import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("AI Network Threat Detection Dashboard")

API_URL = "http://127.0.0.1:8000/predict"

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Upload Network Traffic Data (CSV)")

uploaded_file = st.file_uploader("Upload CSV Data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview")
    st.dataframe(df.head())

    if st.button("Run Detection"):
        # We slice [:41] to ensure we only send the features the model knows
        all_features = df.iloc[:, :41].values.tolist()

        with st.spinner("Analyzing network traffic..."):
            try:
                # ONE single API call for the whole file
                response = requests.post(API_URL, json={"data": all_features})
                result = response.json()

                if "predictions" in result:
                    batch_preds = result["predictions"]
                    
                    # 1. Update the table you see on screen
                    df["Prediction"] = batch_preds
                    
                    # 2. Update the long-term history
                    st.session_state.history.extend(batch_preds)
                    
                    st.success(f"Done! Processed {len(batch_preds)} rows.")

                    # --- RENDER GRAPHS ---
                    st.subheader("Detection Results")
                    st.dataframe(df)

                    st.subheader("Current Batch Analysis")
                    attack_counts = df["Prediction"].value_counts().reset_index()
                    attack_counts.columns = ["Attack Type", "Count"]

                    fig = px.bar(
                        attack_counts, 
                        x="Attack Type", 
                        y="Count", 
                        color="Attack Type",
                        title="Results for this Upload"
                    )
                    st.plotly_chart(fig)
                else:
                    st.error(f"API Error: {result.get('error')}")

            except Exception as e:
                st.error(f"Could not connect to API. Is app.py running? Error: {e}")

# History Dashboard (Outside the upload block so it always shows)
if st.session_state.history:
    st.divider()
    st.subheader("📊 Global Detection History")

    history_df = pd.DataFrame(st.session_state.history, columns=["Attack"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Traffic Checked", len(history_df))
    
    # Matching the case returned by your API
    normal_count = history_df[history_df["Attack"].str.lower() == "normal"].shape[0]
    attack_count = len(history_df) - normal_count
    
    col2.metric("Normal Traffic", normal_count)
    col3.metric("Total Attacks", attack_count)

    # Pie chart
    fig2 = px.pie(
        history_df,
        names="Attack",
        title="Overall Attack Type Distribution",
        hole=0.4
    )
    st.plotly_chart(fig2)

    # Histogram
    fig3 = px.histogram(
        history_df,
        x="Attack",
        title="Attack Frequency History",
        color="Attack"
    )
    st.plotly_chart(fig3)
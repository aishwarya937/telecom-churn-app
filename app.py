import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# 1. LOAD ASSETS
@st.cache_resource
def load_assets():
    model = joblib.load('churn_model.pkl')
    scaler = joblib.load('scaler.pkl')
    features = joblib.load('features.pkl')
    return model, scaler, features

model, scaler, features = load_assets()

# 2. UI LAYOUT
st.set_page_config(page_title="Telecom Churn AI", layout="wide")
st.title("📞 Customer Retention Intelligence System")
st.markdown("---")

# 3. INPUT COLUMNS
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Customer Profile")
    with st.container(border=True):
        tenure = st.slider("Tenure (Months)", 1, 72, 12)
        monthly = st.number_input("Monthly Charges ($)", 18.0, 120.0, 70.0)
        services = st.slider("Total Services Active", 1, 9, 3)
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

# 4. PREDICTION LOGIC
def predict():
    # Create empty row with all features set to 0
    input_df = pd.DataFrame(0, index=[0], columns=features)
    
    # Fill numerical data
    input_df['Tenure Months'] = tenure
    input_df['Monthly Charges'] = monthly
    input_df['Total Charges'] = tenure * monthly
    input_df['Total_Services'] = services
    
    # Map Categoricals (Sets the correct column to 1)
    if f"Contract_{contract}" in features: input_df[f"Contract_{contract}"] = 1
    if f"Internet Service_{internet}" in features: input_df[f"Internet Service_{internet}"] = 1
    if f"Payment Method_{payment}" in features: input_df[f"Payment Method_{payment}"] = 1
    
    # Scale Numerical Columns (must match the training order)
    num_cols = ['Tenure Months', 'Monthly Charges', 'Total Charges', 'Total_Services']
    input_df[num_cols] = scaler.transform(input_df[num_cols])
    
    # Final probability
    prob = model.predict_proba(input_df)[0][1]
    return prob

# 5. DASHBOARD RESULTS
with col2:
    risk_score = predict()
    
    # Professional Gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score * 100,
        title = {'text': "Churn Probability %"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 35], 'color': "#00CC96"}, # Green
                {'range': [35, 70], 'color': "#FFA15A"}, # Orange
                {'range': [70, 100], 'color': "#EF553B"} # Red
            ]}))
    st.plotly_chart(fig, use_container_width=True)
    
    # Business Logic
    ltv = tenure * monthly
    st.subheader("💡 Strategic Insights")
    
    c1, c2 = st.columns(2)
    c1.metric("Customer Lifetime Value", f"${ltv:,.2f}")
    
    if risk_score > 0.7:
        c2.error("URGENT: High Risk")
        st.info("**Retention Strategy:** Offer a 20% loyalty discount if they switch to a 1-year contract today.")
    elif risk_score > 0.4:
        c2.warning("WARNING: Medium Risk")
        st.info("**Retention Strategy:** Send a service quality survey and offer a free 3-month add-on service.")
    else:
        c2.success("STABLE: Low Risk")
        st.info("**Upsell Opportunity:** Excellent candidate for premium technical support or family plans.")
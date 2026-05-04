import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. SETTINGS & SECURITY CREDENTIALS ---
# Replace these with your actual details for a live demo
SENDER_EMAIL = "your-email@gmail.com" 
SENDER_PASSWORD = "your-app-password" # Get this from Google App Passwords
RECEIVER_EMAIL = "your-email@gmail.com" 

# --- 2. ENTERPRISE UI CONFIG & CSS ---
st.set_page_config(page_title="ChurnIntel Pro | Enterprise", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    .stApp { background-color: #f8fafc; }
    
    /* Hero Header */
    .main-header { 
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%); 
        padding: 3rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    /* Ticket Card Styling */
    .ticket-card { 
        background: white; padding: 1.5rem; border-radius: 12px; 
        border-left: 6px solid #2563eb; margin-bottom: 1rem; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
    }

    /* Wobble Animation Logic */
    @keyframes wobble {
      0%, 100% { transform: translateX(0%); }
      15% { transform: translateX(-5px) rotate(-1deg); }
      30% { transform: translateX(3px) rotate(1deg); }
      45% { transform: translateX(-3px) rotate(-1deg); }
    }

    /* Professional Blue Buttons with Wobble */
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        background-color: #2563eb; color: white; font-weight: 700; 
        border: none; transition: 0.3s;
    }
    
    .stButton>button:hover { 
        animation: wobble 0.5s ease-in-out;
        background-color: #1d4ed8 !important;
        box-shadow: 0 8px 15px rgba(37, 99, 235, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE & ASSETS ---
if 'page' not in st.session_state: st.session_state.page = "LANDING"
if 'tickets' not in st.session_state: st.session_state.tickets = []

@st.cache_resource
def load_assets():
    return joblib.load('churn_model.pkl'), joblib.load('scaler.pkl'), joblib.load('features.pkl')

# --- 4. EMAIL LOGIC ---
def send_email_report(ticket_data):
    if not ticket_data:
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"🚨 URGENT: Churn Risk Executive Alert - {datetime.now().strftime('%Y-%m-%d')}"
        
        body = "Executive Summary of High-Risk Customers identified by AI:\n\n"
        for t in ticket_data:
            body += f"Ticket ID: {t['id']} | Risk: {t['risk']:.1%} | Impact: ${t['val']} | Recommendation: {t['rec']}\n"
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

# --- 5. PAGE: PRODUCT LANDING ---
def show_landing():
    st.markdown("""
        <div class="main-header">
            <h1 style='font-size: 3rem;'>ChurnIntel Pro</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Next-Gen Telecom Retention Intelligence & Automated Ticketing System</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.info("### 🧠 AI Churn Engine\nPredict churn with 89% accuracy using optimized Random Forest algorithms."); 
    with c2: st.info("### 🎫 Smart Ticketing\nAutomatically trigger internal service tickets for accounts with Risk > 70%.");
    with c3: st.info("### 📧 Executive Alerts\nInstant email escalation for high-value revenue-at-risk segments."); 
    
    st.write("##")
    _, mid, _ = st.columns([1,1,1])
    with mid:
        if st.button("LAUNCH ENTERPRISE CONSOLE"):
            st.session_state.page = "LOGIN"
            st.rerun()

# --- 6. PAGE: LOGIN ---
def show_login():
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.write("#")
        st.markdown("<h2 style='text-align: center;'>🔐 Secure Portal Access</h2>", unsafe_allow_html=True)
        with st.container(border=True):
            user = st.text_input("User ID (Professional Email)")
            pwd = st.text_input("Security Access Key", type="password")
            if st.button("Authorize Session"):
                if user and pwd:
                    st.session_state.page = "DASHBOARD"
                    st.rerun()

# --- 7. PAGE: EXECUTIVE DASHBOARD ---
def show_dashboard():
    model, scaler, features = load_assets()
    
    st.sidebar.title("💎 ChurnIntel Pro")
    if st.sidebar.button("🎫 Ticket Center"): st.session_state.page = "TICKETS"; st.rerun()
    if st.sidebar.button("🔓 System Logout"): st.session_state.page = "LANDING"; st.rerun()

    st.title("📊 Retention Diagnostics & Analytics")
    
    # Global KPIs
    k1, k2, k3 = st.columns(3)
    k1.metric("National Churn Rate", "14.2%", "-1.1%")
    k2.metric("Revenue at Risk (RaR)", "$42,500", "+$2,1k")
    k3.metric("System Health", "Optimal", "RF-v4 Active")

    st.markdown("---")
    
    col_in, col_out = st.columns([1, 1.5])
    with col_in:
        st.subheader("Account Diagnostics")
        with st.container(border=True):
            tenure = st.slider("Tenure (Months)", 1, 72, 12)
            monthly = st.number_input("Monthly Charges ($)", 18.0, 150.0, 70.0)
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
            internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
            payment = st.selectbox("Billing Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

    with col_out:
        # Prediction Math
        input_df = pd.DataFrame(0, index=[0], columns=features)
        input_df['Tenure Months'], input_df['Monthly Charges'], input_df['Total_Services'] = tenure, monthly, 3
        input_df['Total Charges'] = tenure * monthly
        if f"Contract_{contract}" in features: input_df[f"Contract_{contract}"] = 1
        if f"Internet Service_{internet}" in features: input_df[f"Internet Service_{internet}"] = 1
        if f"Payment Method_{payment}" in features: input_df[f"Payment Method_{payment}"] = 1
        
        num_cols = ['Tenure Months', 'Monthly Charges', 'Total Charges', 'Total_Services']
        input_df[num_cols] = scaler.transform(input_df[num_cols])
        
        prob = model.predict_proba(input_df[features])[0][1]
        
        fig = go.Figure(go.Indicator(mode="gauge+number", value=prob*100, title={'text': "Risk Probability Score %"}, gauge={'axis':{'range':[0,100]}, 'steps':[{'range':[0,30],'color':'#22c55e'},{'range':[30,70],'color':'#f59e0b'},{'range':[70,100],'color':'#ef4444'}], 'bar':{'color':'#1e293b'}}))
        st.plotly_chart(fig, use_container_width=True)

        if prob > 0.7:
            st.error("🚨 CRITICAL RISK: Immediate Intervention Required")
            if st.button("EXECUTE AUTOMATED TICKETING"):
                ticket = {
                    "id": f"TIC-{int(time.time())}", 
                    "risk": prob, 
                    "val": tenure*monthly, 
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "rec": "Immediate 25% Loyalty Upgrade Offer"
                }
                st.session_state.tickets.append(ticket)
                st.toast("Ticket Dispatched to Retention Team!")

# --- 8. PAGE: TICKETING & ALERT CENTER ---
def show_tickets():
    st.title("🎫 Automated Ticketing & Alert Center")
    if st.button("⬅️ Return to Dashboard"): st.session_state.page = "DASHBOARD"; st.rerun()
    
    st.write("---")
    
    if not st.session_state.tickets:
        st.info("System Monitoring Active. No critical risk tickets detected.")
    else:
        # --- DOWNLOAD REPORT FEATURE ---
        df = pd.DataFrame(st.session_state.tickets)
        csv = df.to_csv(index=False).encode('utf-8')
        
        col_dl, col_em = st.columns(2)
        with col_dl:
            st.download_button(label="📥 Download Intelligence Report (CSV)", data=csv, file_name=f"retention_report_{datetime.now().strftime('%Y%m%d')}.csv", mime='text/csv')
        
        with col_em:
            if st.button("📧 Send Executive Email Alert"):
                with st.spinner("Connecting to Secure Mail Server..."):
                    success = send_email_report(st.session_state.tickets)
                    if success:
                        st.success(f"Report dispatched to {RECEIVER_EMAIL}!")
                    else:
                        st.warning("Demo Mode: Email logic ready. (Requires valid SMTP credentials)")

        st.write("##")
        for t in st.session_state.tickets:
            st.markdown(f"""
            <div class="ticket-card">
                <span style='color:#ef4444; font-weight:bold;'>[URGENT]</span> <strong>{t['id']}</strong><br>
                <b>Probability:</b> {t['risk']:.1%} | <b>Revenue at Stake:</b> ${t['val']:.0f}<br>
                <b>Recommended Strategy:</b> {t['rec']}
            </div>
            """, unsafe_allow_html=True)

# --- NAVIGATION CONTROLLER ---
if st.session_state.page == "LANDING": show_landing()
elif st.session_state.page == "LOGIN": show_login()
elif st.session_state.page == "DASHBOARD": show_dashboard()
elif st.session_state.page == "TICKETS": show_tickets()

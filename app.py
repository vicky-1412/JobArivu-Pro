import streamlit as st
import sqlite3
import google.generativeai as genai
from datetime import datetime
import os

# --- 1. CONFIG & AI ---
# Gemini API Key integration
genai.configure(api_key="AIzaSyClu8oAPHUbUuiHBP4s9aqrRNP7tRNRPuI")
ai_model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. DATABASE LOGIC ---
def init_db():
    conn = sqlite3.connect('jobarivu_ultimate_v6.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, edu TEXT, role TEXT, phone TEXT)''')
    # Creating Master Account
    try:
        c.execute("INSERT INTO users VALUES ('master', 'master123', 'Master', 'admin', '000')")
    except: pass 
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('jobarivu_ultimate_v6.db')
    c = conn.cursor()
    c.execute("SELECT username, edu, phone FROM users WHERE role='user'")
    data = c.fetchall()
    conn.close()
    return data

# --- 3. UI DESIGN (iPhone Glassmorphism) ---
st.set_page_config(page_title="JobArivu Master", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        color: white;
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.6);
        margin-bottom: 25px;
    }
    .live-info {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px 25px;
        border-radius: 50px;
        text-align: center;
        color: white;
        font-weight: bold;
        border: 1px solid rgba(255,255,255,0.2);
    }
    h1, h2, h3, p, label { color: white !important; }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white; border-radius: 12px; font-weight: bold; border: none; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LIVE HEADER (Time, Date, Weather) ---
t_col1, t_col2 = st.columns([2, 1])
with t_col1:
    st.markdown(f"### 💎 JobArivu Pro Master")
with t_col2:
    now = datetime.now()
    st.markdown(f"""
        <div class="live-info">
            🕒 {now.strftime('%H:%M')} | 📅 {now.strftime('%d %b')} | 🌡️ 29°C ☀️ Rameswaram
        </div>
    """, unsafe_allow_html=True)

init_db()
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- 5. AUTHENTICATION ---
if not st.session_state["logged_in"]:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📱 Phone OTP Login")
        phone = st.text_input("Phone Number")
        if st.button("Send OTP"): st.success("OTP Sent (Test Code: 1234)")
        otp = st.text_input("Enter 4-digit OTP", type="password")
        if st.button("Verify & Login"):
            if otp == "1234":
                st.session_state["logged_in"] = True
                st.session_state["role"] = "user"
                st.session_state["user"] = phone
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("👑 Master Access")
        mu = st.text_input("Admin Username")
        mp = st.text_input("Admin Password", type="password")
        if st.button("Login as Master"):
            if mu == "master" and mp == "master123":
                st.session_state["logged_in"] = True
                st.session_state["role"] = "admin"
                st.session_state["user"] = "Master"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🌐 Social Login")
        if st.button("Continue with Facebook"):
            st.session_state["logged_in"] = True
            st.session_state["role"] = "user"
            st.session_state["user"] = "FB User"
            st.rerun()
        if st.button("Login via WhatsApp"):
            st.session_state["logged_in"] = True
            st.session_state["role"] = "user"
            st.session_state["user"] = "WA User"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. DASHBOARDS ---
else:
    if st.session_state["role"] == "admin":
        st.title("👑 Master Control Dashboard")
        users = get_all_users()
        st.markdown(f'<div class="glass-card"><h2>Total Active Users: {len(users)}</h2></div>', unsafe_allow_html=True)
        
        for user in users:
            with st.expander(f"👤 {user[0]}"):
                st.write(f"Qualification: {user[1]} | Phone: {user[2]}")
                st.button(f"Alert {user[0]}", key=user[0])
    
    else:
        st.title(f"Vannakam, {st.session_state['user']} ✨")
        # FIX: Multi-line triple quotes correctly closed here
        st.markdown(f"""
        <div class="glass-card">
            <h2>User Dashboard</h2>
            <p>Welcome to your personal career portal.</p>
        </div>
        """, unsafe_allow_html=True)

    if st.sidebar.button("Logout & Exit"):
        st.session_state["logged_in"] = False
        st.rerun()
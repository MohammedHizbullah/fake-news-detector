# ✅ SUPERCOOL FAKE NEWS DETECTOR APP (OFFLINE EDITION + LOCAL LOGIN)

import streamlit as st
import pickle
import requests
import pandas as pd
import sqlite3
import hashlib

# --- CONFIG ---
st.set_page_config(page_title="Fake News Detector", page_icon="🔮", layout="centered")

# --- CUSTOM STYLING FOR LOGIN UI ---
login_css = """
<style>
html, body, [class*="css"]  {
    background-color: #0f172a;
    color: #e0f7fa;
    font-family: 'Segoe UI', sans-serif;
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
  from {opacity: 0; transform: translateY(-10px);}
  to {opacity: 1; transform: translateY(0);}
}

h1 {
    text-align: center;
    color: #00ffc6;
    text-shadow: 0px 0px 10px #00ffc6;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

label, .stTextInput > div > input {
    color: #f1f5f9;
}

.stTextInput > div > input, .stTextArea > div > textarea {
    background-color: #1e293b;
    border: 1px solid #38bdf8;
    border-radius: 8px;
    padding: 10px;
}

.stButton > button {
    background: linear-gradient(to right, #06b6d4, #3b82f6);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    box-shadow: 0px 0px 10px rgba(0, 255, 255, 0.4);
    margin-top: 10px;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(to right, #3b82f6, #06b6d4);
}
</style>
"""
st.markdown(login_css, unsafe_allow_html=True)

# --- DB SETUP ---
def create_usertable():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def add_userdata(username, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, email, password) VALUES (?, ?, ?)', (username, email, password))
    conn.commit()
    conn.close()

def login_user(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    data = c.fetchone()
    conn.close()
    return data

create_usertable()

# --- LOGIN PAGE ---
def login_page():
    st.markdown("<h1>🔐 Login to Continue</h1>", unsafe_allow_html=True)
    choice = st.radio("Select", ["Login", "Signup"])

    if choice == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            result = login_user(email, password)
            if result:
                st.session_state.logged_in = True
                st.session_state.username = result[0]
                st.success("Login successful!")
            else:
                st.error("Invalid Credentials")

    else:
        email = st.text_input("Email")
        password = st.text_input("Create Password", type="password")
        username = st.text_input("Username")
        if st.button("Signup"):
            add_userdata(username, email, password)
            st.success("Account created successfully! You can now log in.")

# --- AUTH CHECK ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
    st.stop()


# --- MAIN APP STARTS ---
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

GNEWS_API_KEY = "da8e9a69097dee5d1aaf671b363a5b42"

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.title("🛠 Options")
category = st.sidebar.selectbox("News Category", ["general", "technology", "sports", "science", "business", "entertainment", "health"])
country = st.sidebar.selectbox("Country", ["in", "us", "gb", "ca", "au"])

st.markdown("""
<h1 style='text-align: center;'>🔮 AI FAKE NEWS DETECTOR</h1>
<h3 class='typing' style='text-align: center; color: #7dd3fc;'>Decoding the truth, one headline at a time.</h3>
<hr>
""", unsafe_allow_html=True)

st.header("🎯 Predict From Text")
text_input = st.text_area("Paste article or headline here:")
if st.button("🔥 Predict Now"):
    if text_input.strip():
        with st.spinner("Analyzing with AI magic... 🧪"):
            vec = vectorizer.transform([text_input])
            pred = model.predict(vec)[0]
            prob = model.predict_proba(vec)[0]
            confidence = prob[1] if pred == 1 else prob[0]
            label = "🟢 Real" if pred == 1 else "🔴 Fake"
        st.metric("Prediction", label)
        st.progress(int(confidence * 100))
        st.session_state.history.append({"type": "User Text", "text": text_input, "label": label, "confidence": f"{confidence*100:.2f}%"})
    else:
        st.warning("Please enter some text.")

st.header("🛰️ Scan Live News")
if st.button("📡 Fetch Headlines"):
    try:
        url = f"https://gnews.io/api/v4/top-headlines?lang=en&max=10&country={country}&topic={category}&token={GNEWS_API_KEY}"
        res = requests.get(url).json()
        if "articles" in res:
            for article in res["articles"]:
                title = article["title"]
                vec = vectorizer.transform([title])
                pred = model.predict(vec)[0]
                prob = model.predict_proba(vec)[0]
                conf = prob[1] if pred == 1 else prob[0]
                label = "🟢 Real" if pred == 1 else "🔴 Fake"
                st.write(f"**{title}** → {label} ({conf*100:.2f}%)")
                st.session_state.history.append({"type": "Live News", "text": title, "label": label, "confidence": f"{conf*100:.2f}%"})
        else:
            st.error("No headlines found or API limit exceeded.")
    except Exception as e:
        st.error("Failed to fetch headlines.")
        st.caption(str(e))

st.header("📁 Upload Headlines")
uploaded = st.file_uploader("Upload .txt or .csv file (one headline per line)", type=["txt", "csv"])
if uploaded:
    try:
        if uploaded.name.endswith(".txt"):
            lines = uploaded.read().decode("utf-8").splitlines()
        else:
            df = pd.read_csv(uploaded)
            lines = df.iloc[:, 0].dropna().tolist()
        for line in lines:
            vec = vectorizer.transform([line])
            pred = model.predict(vec)[0]
            prob = model.predict_proba(vec)[0]
            conf = prob[1] if pred == 1 else prob[0]
            label = "🟢 Real" if pred == 1 else "🔴 Fake"
            st.write(f"**{line}** → {label} ({conf*100:.2f}%)")
            st.session_state.history.append({"type": "Uploaded", "text": line, "label": label, "confidence": f"{conf*100:.2f}%"})
    except Exception as e:
        st.error("Error processing file.")
        st.caption(str(e))

st.header("📜 Prediction History")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)
    report_text = "\n\n".join([f"[{row['type']}] {row['text']}\n→ {row['label']} ({row['confidence']})" for i, row in df.iterrows()])
    st.download_button("📄 Download Full Report", data=report_text, file_name="fake_news_report.txt")
else:
    st.info("No predictions yet. Enter text, scan news, or upload a file to begin.")

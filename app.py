# ✅ SUPERCOOL FAKE NEWS DETECTOR APP (ULTRA EDITION)

import streamlit as st
import pickle
import requests
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Fake News Detector", page_icon="🔮", layout="wide")

# --- LOAD MODEL ---
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

GNEWS_API_KEY = "da8e9a69097dee5d1aaf671b363a5b42"

if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR OPTIONS ---
st.sidebar.title("🛠 Options")
category = st.sidebar.selectbox("News Category", ["general", "technology", "sports", "science", "business", "entertainment", "health"])
country = st.sidebar.selectbox("Country", ["in", "us", "gb", "ca", "au"])

# --- STYLING ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
<style>
html, body {
    background: radial-gradient(circle at top left, #1e293b, #0f172a);
    color: #e0f7fa;
    font-family: 'Orbitron', sans-serif;
    overflow-x: hidden;
}

body::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: url('https://www.transparenttextures.com/patterns/stardust.png');
    opacity: 0.04;
    z-index: -1;
}

h1, h2, h3 {
    text-transform: uppercase;
    color: #0ff;
    text-shadow: 0 0 10px #0ff, 0 0 20px #0ff;
    letter-spacing: 2px;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from { text-shadow: 0 0 5px #0ff, 0 0 10px #0ff; }
  to { text-shadow: 0 0 15px #0ff, 0 0 30px #0ff; }
}

.typing {
  overflow: hidden;
  white-space: nowrap;
  border-right: 2px solid #0ff;
  width: 0;
  animation: typing 4s steps(40, end) forwards;
}

@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}

textarea, .stTextInput > div > input {
    background-color: #111827;
    color: #0ff;
    border: 2px dashed #38bdf8;
    border-radius: 10px;
    padding: 12px;
    font-size: 16px;
    transition: all 0.3s;
}

.stButton > button {
    background: linear-gradient(to right, #8b5cf6, #ec4899);
    color: #fff;
    font-weight: bold;
    border-radius: 15px;
    padding: 12px 30px;
    box-shadow: 0 0 25px #8b5cf6;
    text-transform: uppercase;
    animation: pulse 2s infinite;
    transition: transform 0.3s ease;
}

@keyframes pulse {
  0% { box-shadow: 0 0 10px #8b5cf6; }
  50% { box-shadow: 0 0 20px #ec4899; }
  100% { box-shadow: 0 0 10px #8b5cf6; }
}

.stButton > button:hover {
    transform: scale(1.07);
    background: linear-gradient(to right, #ec4899, #8b5cf6);
}

.stProgress > div > div > div {
    background: linear-gradient(to right, #34d399, #10b981);
}

.metric-label, .metric-value {
    font-size: 1.5rem;
    color: #fff;
    text-shadow: 0 0 8px #00ffcc;
}

.dataframe tbody tr:nth-child(even) {
    background-color: #1e293b;
}
.dataframe tbody tr:nth-child(odd) {
    background-color: #0f172a;
}
.dataframe tbody tr:hover {
    background-color: #334155;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<h1 style='text-align: center;'>🔮 AI FAKE NEWS DETECTOR</h1>
<h3 class='typing' style='text-align: center; color: #7dd3fc;'>Decoding the truth, one headline at a time.</h3>
<hr>
""", unsafe_allow_html=True)

# --- TEXT PREDICTION ---
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

# --- LIVE NEWS ---
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

# --- FILE UPLOAD ---
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

# --- HISTORY ---
st.header("📜 Prediction History")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)
    report_text = "\n\n".join([f"[{row['type']}] {row['text']}\n→ {row['label']} ({row['confidence']})" for i, row in df.iterrows()])
    st.download_button("📄 Download Full Report", data=report_text, file_name="fake_news_report.txt")
else:
    st.info("No predictions yet. Enter text, scan news, or upload a file to begin.")

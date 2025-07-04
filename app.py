# ✅ UPGRADED FAKE NEWS DETECTOR APP

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

GNEWS_API_KEY = "YOUR_GNEWS_API_KEY"

# --- INIT SESSION ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR ---
st.sidebar.title("🛠 Options")
category = st.sidebar.selectbox("News Category", ["general", "technology", "sports", "science", "business", "entertainment", "health"])
country = st.sidebar.selectbox("Country", ["in", "us", "gb", "ca", "au"])
dark_mode = st.sidebar.checkbox("Dark Mode")

# --- ADVANCED CSS ---
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #1c1c1c, #2e2e2e);
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3, h4, h5 {
    color: #00ffdd;
    font-weight: 700;
}

.css-18e3th9 {
    padding: 3rem 1rem 1rem 1rem;
    background: #101010;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(0, 255, 221, 0.3);
}

.stButton > button {
    background: linear-gradient(to right, #00f5c9, #00c9ff);
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: bold;
    color: #000000;
    box-shadow: 0 5px 15px rgba(0, 255, 221, 0.3);
    transition: all 0.3s ease-in-out;
}

.stButton > button:hover {
    background: linear-gradient(to right, #00c9ff, #00f5c9);
    transform: scale(1.05);
}

textarea, input[type="text"] {
    background-color: #2c2c2c;
    color: #ffffff;
    border: 1px solid #00ffdd;
    border-radius: 10px;
    padding: 10px;
}

.css-1cpxqw2 {
    background-color: #2c2c2c !important;
}

.stProgress > div > div > div {
    background-image: linear-gradient(to right, #ff416c, #ff4b2b);
}

.dataframe tbody tr:nth-child(even) {
    background-color: #1f1f1f;
}

.dataframe tbody tr:hover {
    background-color: #333333;
}

footer, header, .reportview-container .main footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# --- MAIN UI ---
st.title("🔮 Fake News Detector")
st.markdown("Use AI to detect whether a news article is real or fake. You can enter text, scan headlines, or upload files.")

# --- TEXT PREDICTION ---
st.header("🔮 Enter News Article")
text_input = st.text_area("Paste article or headline here:")

if st.button("Predict Text"):
    if text_input.strip():
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

# --- GNEWS SCAN ---
st.header("📰 Scan Live News")
if st.button("Fetch Headlines"):
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

# --- BATCH FILE UPLOAD ---
st.header("📁 Upload News Headlines File")
uploaded = st.file_uploader("Upload a .txt or .csv file (one headline per line)", type=["txt", "csv"])

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

# --- HISTORY LOG ---
st.header("📜 Prediction History")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

    report_text = "\n\n".join([f"[{row['type']}] {row['text']}\n→ {row['label']} ({row['confidence']})" for i, row in df.iterrows()])
    st.download_button("📄 Download Report", data=report_text, file_name="fake_news_report.txt")
else:
    st.info("No predictions yet. Enter text, scan news or upload a file to begin.")

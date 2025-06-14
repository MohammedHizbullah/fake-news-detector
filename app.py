import streamlit as st
import pickle

# Page Configuration
st.set_page_config(page_title="Fake News Detector", page_icon="🧠", layout="centered")

# Load Model and Vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# --- Elegant CSS Styling ---
st.markdown("""
<style>
/* Body background */
html, body, [class*="css"] {
    background-color: #12181b;
    font-family: 'Segoe UI', sans-serif;
    color: #f5f5f5;
}

/* Title Gradient */
.main-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: bold;
    background: linear-gradient(to right, #00f5c9, #ff416c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}

/* Subtitle */
.subtext {
    text-align: center;
    font-size: 1.1rem;
    color: #bbbbbb;
    margin-bottom: 2rem;
}

/* Input box */
.stTextArea textarea {
    background-color: #1d2228 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    padding: 15px !important;
    font-size: 1rem !important;
    border: 1px solid #444 !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Button style */
.stButton > button {
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: white;
    font-weight: 600;
    font-size: 1rem;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    margin-top: 15px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(0,0,0,0.25);
}

.stButton > button:hover {
    background: linear-gradient(to right, #ff4b2b, #ff416c);
    transform: scale(1.03);
}

/* Result card */
.result-box {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid #444;
    padding: 1.2rem;
    border-radius: 12px;
    margin-top: 1.5rem;
    text-align: center;
    font-size: 1.2rem;
}

/* Footer */
.footer {
    margin-top: 3rem;
    text-align: center;
    font-size: 0.85rem;
    color: #888888;
}
</style>
""", unsafe_allow_html=True)

# --- Page UI ---
st.markdown("<div class='main-title'>🧠 Fake News Detector</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Check whether a news article is real or fake using AI</div>", unsafe_allow_html=True)

text_input = st.text_area("📝 Enter the news article text below:")

# --- Prediction ---
if st.button("🔍 Predict"):
    if text_input.strip():
        vec_input = vectorizer.transform([text_input])
        prediction = model.predict(vec_input)
        if prediction == 1:
            st.markdown(f"<div class='result-box'>🟢 <strong>Real News</strong></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-box'>🔴 <strong>Fake News</strong></div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter some text to analyze.")

# --- Footer ---
st.markdown("<div class='footer'>Made with ❤️ by Mohammed Hizbullah | Powered by Streamlit</div>", unsafe_allow_html=True)

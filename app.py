import streamlit as st
from transformers import pipeline

# Page Configuration
st.set_page_config(page_title="Fake News Detector", page_icon="🧠", layout="centered")

# Load BERT model (multilingual)
classifier = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Elegant CSS Styling
st.markdown("""
<style>
body {
    background-color: #0f1117;
    color: #f1f1f1;
    font-family: 'Segoe UI', sans-serif;
}

.main-title {
    text-align: center;
    font-size: 3.5rem;
    background: -webkit-linear-gradient(45deg, #00ffe7, #ff4b4b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    font-weight: bold;
}

.subtext {
    text-align: center;
    font-size: 1.1rem;
    color: #bbbbbb;
    margin-bottom: 2rem;
}

.stTextArea textarea {
    background-color: rgba(30, 34, 45, 0.7) !important;
    color: #ffffff !important;
    border-radius: 10px;
    font-size: 1.05rem;
    padding: 15px;
}

.stButton>button {
    background: linear-gradient(90deg, #ff4b4b, #ff8c42);
    color: white;
    font-weight: bold;
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 12px;
    transition: 0.3s ease;
    font-size: 1.1rem;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #ff8c42, #ff4b4b);
    transform: scale(1.03);
}

.result-box {
    background: rgba(255, 255, 255, 0.05);
    padding: 1.2rem;
    border-radius: 12px;
    margin-top: 1.5rem;
    text-align: center;
    font-size: 1.2rem;
    border: 1px solid #555;
}

.footer {
    margin-top: 3rem;
    text-align: center;
    font-size: 0.9rem;
    color: #888888;
}
</style>
""", unsafe_allow_html=True)

# --- UI Content ---
st.markdown("<div class='main-title'>🧠 Fake News Detector</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Check whether a news article is real or fake using AI-powered analysis</div>", unsafe_allow_html=True)

text_input = st.text_area("📝 Enter the news article text below:")

# Prediction
if st.button("🔍 Predict"):
    if text_input.strip():
        try:
            result = classifier(text_input)[0]
            label = result['label']
            score = result['score'] * 100

            if "4" in label or "5" in label:
                st.markdown(f"<div class='result-box'>🟢 <b>Real News</b><br>({label}, {score:.2f}% confidence)</div>", unsafe_allow_html=True)
            elif "1" in label or "2" in label:
                st.markdown(f"<div class='result-box'>🔴 <b>Fake News</b><br>({label}, {score:.2f}% confidence)</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='result-box'>🟡 <b>Uncertain</b><br>({label}, {score:.2f}% confidence)</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("❌ Error: Unable to process this input. Try shorter or English headline.")
            st.caption(f"Details: {e}")
    else:
        st.warning("⚠️ Please enter some text.")

# Footer
st.markdown("<div class='footer'>Made with ❤️ by Mohammed Hizbullah | Powered by Streamlit</div>", unsafe_allow_html=True)

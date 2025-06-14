import streamlit as st

# Custom Page Config
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="🧠",
    layout="centered"
)

from transformers import pipeline
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #0f1117;
        color: #f1f1f1;
        font-family: 'Segoe UI', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        color: #FF6B6B;
        margin-bottom: 0.5rem;
    }

    .subtext {
        text-align: center;
        color: #c0c0c0;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    .stTextArea textarea {
        background-color: #1e222d !important;
        color: #ffffff !important;
    }

    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        margin-top: 10px;
    }

    .footer {
        margin-top: 3rem;
        text-align: center;
        font-size: 0.9rem;
        color: #aaaaaa;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI ---
st.markdown("<div class='main-title'>🧠 Fake News Detector</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Check whether a news article is real or fake using AI</div>", unsafe_allow_html=True)

# Text input
text_input = st.text_area("Enter the news article text below 👇")

# Prediction using BERT
if st.button("🔍 Predict"):
    if text_input.strip():
        output = classifier(text_input)[0]
        label = "🟢 This appears to be Real News." if output['label'] == "POSITIVE" else "🔴 This appears to be Fake News."
        confidence = output['score'] * 100
        st.success(f"{label} ({confidence:.2f}% confidence)")
    else:
        st.warning("⚠️ Please enter some text to analyze.")


# Footer
st.markdown("<div class='footer'>Made with ❤️ by Mohammed Hizbullah | Powered by Streamlit</div>", unsafe_allow_html=True)

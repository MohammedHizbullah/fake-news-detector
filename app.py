import streamlit as st

# Custom Page Config
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="🧠",
    layout="centered"
)

from transformers import pipeline
classifier = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")


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
        try:
            result = classifier(text_input)[0]
            label = result['label']
            score = result['score'] * 100

            if "4" in label or "5" in label:
                st.success(f"🟢 Real News ({label}, {score:.2f}% confidence)")
            elif "1" in label or "2" in label:
                st.error(f"🔴 Fake News ({label}, {score:.2f}% confidence)")
            else:
                st.info(f"🟡 Uncertain ({label}, {score:.2f}% confidence)")
        except Exception as e:
            st.error("❌ Error: Unable to process this input. Try a shorter or English headline.")
            st.caption(f"Details: {e}")
    else:
        st.warning("⚠️ Please enter some text.")



# Footer
st.markdown("<div class='footer'>Made with ❤️ by Mohammed Hizbullah | Powered by Streamlit</div>", unsafe_allow_html=True)

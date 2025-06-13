import streamlit as st
import pickle

# Load model and vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Custom HTML title and styles
st.markdown("""
    <style>
        .main-title {
            font-size: 3em;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }
        .description {
            text-align: center;
            font-size: 1.2em;
            color: #555;
        }
        .stTextArea label {
            font-weight: bold;
            color: #333;
        }
        .prediction-box {
            padding: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
            text-align: center;
            font-size: 1.3em;
            font-weight: bold;
        }
        .real {
            color: green;
        }
        .fake {
            color: red;
        }
    </style>

    <div class="main-title">🧠 Fake News Detector</div>
    <div class="description">Check if a news article is real or fake using AI!</div>
    <br>
""", unsafe_allow_html=True)

text = st.text_area("Enter the news article text below:")

if st.button("🔍 Predict"):
    if text.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:
        vec = vectorizer.transform([text])
        result = model.predict(vec)[0]

        label = "✅ Real News" if result == 1 else "❌ Fake News"
        color_class = "real" if result == 1 else "fake"

        import io

if st.button("⬇️ Download Report"):
    report = f"""Fake News Detector Report

Input Text:
{text}

Prediction:
{"Real News" if result == 1 else "Fake News"}
"""
    st.download_button("Download as TXT", data=report, file_name="report.txt")


        st.markdown(f"""
        <div class="prediction-box {color_class}">
            {label}
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<hr>
<center>
    <small>Made with ❤️ by Mohammed Hizbullah | Powered by Streamlit</small>
</center>
""", unsafe_allow_html=True)

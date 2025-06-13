import streamlit as st
import pickle

# Load model and vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

st.title("📰 Fake News Detector")

text = st.text_area("Enter news article text here")

if st.button("Predict"):
    vec = vectorizer.transform([text])
    result = model.predict(vec)[0]
    st.success("✅ Real News" if result == 1 else "❌ Fake News")

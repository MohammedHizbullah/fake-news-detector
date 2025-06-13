import streamlit as st

st.title("📄 About the Fake News Detector")

st.markdown("""
This app uses a **Machine Learning model** (Logistic Regression or similar) trained on a dataset of fake and real news headlines.

### 🔍 How It Works
- Text is transformed using **TF-IDF vectorization**
- The model predicts whether it’s likely **real or fake**

### 📊 Tech Stack
- **Python**
- **Scikit-learn**
- **Streamlit**
- **Natural Language Processing (NLP)**

---

### 👤 Developer
**Mohammed Hizbullah**  
B.Tech IT @ B.S. Abdur Rahman Crescent Institute, Chennai  
GitHub: [@MohammedHizbullah](https://github.com/MohammedHizbullah)
""")

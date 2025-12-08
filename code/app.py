# streamlit_app.py

import streamlit as st
import pandas as pd
import os

# ----------------------------
# Placeholder imports (replace with your notebook code)
# ----------------------------
# from kiro import KiroClient
# from sentiment import run_sentiment_pipeline   # your refactored notebook code
# import openai

# ----------------------------
# App Title + Description
# ----------------------------
st.set_page_config(page_title="Airbnb Sentiment Analyzer", layout="wide")

st.title("🏠 Airbnb Review Sentiment Analyzer")
st.write("""
Use this app to analyze sentiment and tone from Airbnb reviews using **Kiro** + **OpenAI**.
Upload a CSV file or paste a review manually.
""")

# ----------------------------
# Sidebar – Settings & API Keys
# ----------------------------
st.sidebar.header("App Configuration")

openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
kiro_key = st.sidebar.text_input("Kiro API Key", type="password")

run_button = st.sidebar.button("Run Analysis")

if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key

# ----------------------------
# Input Section
# ----------------------------
st.subheader("1. Input Review Text")

input_mode = st.radio("Choose input method:", ["Paste Text", "Upload CSV"])

review_text = None
uploaded_df = None

if input_mode == "Paste Text":
    review_text = st.text_area(
        "Paste an Airbnb review:",
        height=150,
        placeholder="e.g., The place was clean, but the host was rude..."
    )

elif input_mode == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file with a 'review' column", type=["csv"])
    if uploaded_file:
        uploaded_df = pd.read_csv(uploaded_file)
        st.dataframe(uploaded_df.head())

# ----------------------------
# Run Sentiment Analysis
# ----------------------------
st.subheader("2. Sentiment Analysis Results")

if run_button:
    if not (openai_key and kiro_key):
        st.error("Please enter both OpenAI and Kiro API keys.")
    else:
        with st.spinner("Running sentiment analysis..."):
            
            # ------------------------------------
            # 📌 Call your pipeline here
            # result = run_sentiment_pipeline(review_text or uploaded_df)
            # ------------------------------------

            # Placeholder mock response
            result = {
                "sentiment": "positive",
                "score": 0.87,
                "explanation": "The review expresses satisfaction with the stay overall."
            }

        # ----------------------------
        # Display results
        # ----------------------------
        st.success("Analysis Complete!")

        if input_mode == "Paste Text" and review_text:
            st.write("### Sentiment:", result["sentiment"])
            st.write("### Score:", result["score"])
            st.write("### Explanation:")
            st.write(result["explanation"])

        elif uploaded_df is not None:
            st.write("### Batch Processing Preview")
            st.write(result)   # Replace with DF of results


# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Kiro + OpenAI + Streamlit.")

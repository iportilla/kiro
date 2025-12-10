# streamlit_app.py

import streamlit as st
import pandas as pd
import os
from sentiment_analysis import Config, PromptEngine, OpenAIClient, batch_predict

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
kiro_key = st.sidebar.text_input("Kiro API Key", type="password", help="Not currently used in this version")

model_name = st.sidebar.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"], index=0)

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
    uploaded_file = st.file_uploader("Upload a CSV file with a 'comments' column", type=["csv"])
    if uploaded_file:
        uploaded_df = pd.read_csv(uploaded_file)
        st.dataframe(uploaded_df.head())

# ----------------------------
# Run Sentiment Analysis
# ----------------------------
st.subheader("2. Sentiment Analysis Results")

if run_button:
    if not openai_key:
        st.error("Please enter your OpenAI API key.")
    else:
        # Initialize components
        try:
            config = Config(api_key=openai_key, model_name=model_name)
            prompt_engine = PromptEngine()
            client = OpenAIClient(api_key=openai_key, model=model_name, config=config)
            
            with st.spinner("Running sentiment analysis..."):
                results = []
                
                if input_mode == "Paste Text" and review_text:
                    # Single prediction
                    messages = prompt_engine.build_prompt(review_text)
                    result = client.predict_sentiment(review_text, messages)
                    results.append(result)
                    
                elif input_mode == "Upload CSV" and uploaded_df is not None:
                    # Batch prediction
                    if 'comments' in uploaded_df.columns:
                        comments = uploaded_df['comments'].dropna().astype(str).tolist()
                        # Limit for demo purposes to avoid huge bills unexpectedly
                        if len(comments) > 20:
                             st.warning("Limiting analysis to first 20 reviews for demo purposes.")
                             comments = comments[:20]
                        
                        # Use a progress bar
                        progress_bar = st.progress(0)
                        
                        for i, comment in enumerate(comments):
                             messages = prompt_engine.build_prompt(comment)
                             res = client.predict_sentiment(comment, messages)
                             results.append(res)
                             progress_bar.progress((i + 1) / len(comments))
                             
                    else:
                        st.error("CSV must contain a 'comments' column.")
                
                if results:
                    st.success("Analysis Complete!")
                    
                    if input_mode == "Paste Text":
                        res = results[0]
                        if res.get("error"):
                            st.error(f"Error: {res['error']}")
                        else:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Sentiment", res["explanation"].split(" ")[-1])
                            with col2:
                                st.metric("Score", res["sentiment"])
                            with col3:
                                st.metric("Tokens Used", res["input_tokens"] + res["output_tokens"])
                            
                            st.write("### Explanation:")
                            st.write(res["explanation"])
                            
                    elif input_mode == "Upload CSV":
                        results_df = pd.DataFrame(results)
                        st.write("### Batch Processing Results")
                        st.dataframe(results_df)
                        
                        # Simple stats
                        st.write("### Distribution")
                        st.bar_chart(results_df['sentiment'].value_counts())
        
        except Exception as e:
            st.error(f"An error occurred during initialization or processing: {str(e)}")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Kiro + OpenAI + Streamlit.")

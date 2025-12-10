"""
Simplified Streamlit UI for Airbnb Sentiment Analysis
Focus: Simplicity, Performance, User Experience

Key improvements over app.py:
- Session state caching for better performance
- Auto-run on input (no separate button needed)
- Simplified layout with cleaner UI
- Faster rendering with optimized widgets
- Better error handling and user feedback
"""

import streamlit as st
import pandas as pd
import os
from sentiment_analysis import Config, PromptEngine, OpenAIClient

# Page configuration
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🏠",
    layout="centered",  # Centered for better focus
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.prompt_engine = PromptEngine()
    st.session_state.total_cost = 0.0
    st.session_state.total_tokens = 0

# Title
st.title("🏠 Sentiment Analyzer")
st.caption("Analyze Airbnb reviews with OpenAI")

# API Key input (compact, at top)
with st.expander("⚙️ Configuration", expanded=not st.session_state.initialized):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Your API key is not stored"
        )
    
    with col2:
        model = st.selectbox(
            "Model",
            ["gpt-3.5-turbo", "gpt-4"],
            index=0,
            help="gpt-3.5-turbo is faster and cheaper"
        )
    
    if api_key:
        st.session_state.initialized = True
        st.success("✓ Ready to analyze")

# Main content - only show if API key is provided
if not api_key:
    st.info("👆 Enter your OpenAI API key to get started")
    st.stop()

# Set API key in environment
os.environ["OPENAI_API_KEY"] = api_key

# Initialize client (cached in session state)
@st.cache_resource
def get_client(_api_key, _model):
    """Cache the OpenAI client to avoid re-initialization"""
    config = Config(api_key=_api_key, model_name=_model)
    return OpenAIClient(api_key=_api_key, model=_model, config=config), config

try:
    client, config = get_client(api_key, model)
except Exception as e:
    st.error(f"❌ Error initializing: {str(e)}")
    st.stop()

# Input tabs for cleaner organization
tab1, tab2 = st.tabs(["📝 Single Review", "📊 Batch CSV"])

# Tab 1: Single Review
with tab1:
    review_text = st.text_area(
        "Paste review text:",
        height=120,
        placeholder="e.g., Great location! The apartment was clean and the host was very responsive.",
        key="single_review"
    )
    
    if review_text and len(review_text.strip()) > 10:
        # Auto-analyze when text is entered
        with st.spinner("Analyzing..."):
            try:
                messages = st.session_state.prompt_engine.build_prompt(review_text)
                result = client.predict_sentiment(review_text, messages)
                
                if result.get("error"):
                    st.error(f"❌ {result['error']}")
                else:
                    # Update session totals
                    st.session_state.total_tokens += result["input_tokens"] + result["output_tokens"]
                    
                    # Pricing
                    pricing = {"gpt-3.5-turbo": 0.0015, "gpt-4": 0.03}
                    cost = (result["input_tokens"] / 1000) * pricing.get(model, 0.0015)
                    st.session_state.total_cost += cost
                    
                    # Display results in clean format
                    sentiment_map = {1: ("Positive", "😊", "success"), 0: ("Neutral", "😐", "info"), -1: ("Negative", "😞", "error")}
                    label, emoji, status = sentiment_map.get(result["sentiment"], ("Unknown", "🤔", "warning"))
                    
                    st.markdown(f"### {emoji} {label}")
                    st.caption(result["explanation"])
                    
                    # Compact metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Score", result["sentiment"])
                    col2.metric("Tokens", result["input_tokens"] + result["output_tokens"])
                    col3.metric("Cost", f"${cost:.4f}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif review_text:
        st.warning("⚠️ Review must be at least 10 characters")

# Tab 2: Batch CSV
with tab2:
    uploaded_file = st.file_uploader(
        "Upload CSV with 'comments' column",
        type=["csv"],
        help="Max 20 reviews for demo"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            if 'comments' not in df.columns:
                st.error(f"❌ CSV must have 'comments' column. Found: {', '.join(df.columns)}")
            else:
                comments = df['comments'].dropna().astype(str).tolist()
                
                # Show preview
                st.caption(f"Found {len(comments)} reviews")
                with st.expander("Preview data"):
                    st.dataframe(df.head(3), use_container_width=True)
                
                # Limit to 20
                if len(comments) > 20:
                    st.warning(f"⚠️ Processing first 20 of {len(comments)} reviews")
                    comments = comments[:20]
                
                # Process button
                if st.button("🚀 Analyze All", type="primary", use_container_width=True):
                    results = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, comment in enumerate(comments):
                        status_text.text(f"Processing {i+1}/{len(comments)}...")
                        
                        messages = st.session_state.prompt_engine.build_prompt(comment)
                        result = client.predict_sentiment(comment, messages)
                        results.append(result)
                        
                        # Update totals
                        st.session_state.total_tokens += result["input_tokens"] + result["output_tokens"]
                        
                        progress_bar.progress((i + 1) / len(comments))
                    
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Results
                    results_df = pd.DataFrame(results)
                    
                    # Summary metrics
                    st.success("✅ Analysis complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    sentiment_counts = results_df['sentiment'].value_counts()
                    col1.metric("😊 Positive", sentiment_counts.get(1, 0))
                    col2.metric("😐 Neutral", sentiment_counts.get(0, 0))
                    col3.metric("😞 Negative", sentiment_counts.get(-1, 0))
                    
                    # Distribution chart
                    st.bar_chart(sentiment_counts)
                    
                    # Detailed results
                    with st.expander("📋 View all results"):
                        st.dataframe(
                            results_df[['comment', 'sentiment', 'explanation', 'input_tokens', 'output_tokens']],
                            use_container_width=True
                        )
                    
                    # Download button
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        "⬇️ Download Results",
                        csv,
                        "sentiment_results.csv",
                        "text/csv",
                        use_container_width=True
                    )
        
        except Exception as e:
            st.error(f"❌ Error processing CSV: {str(e)}")

# Footer with session stats
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.caption(f"💰 Session cost: ${st.session_state.total_cost:.4f}")
with col2:
    st.caption(f"🎯 Total tokens: {st.session_state.total_tokens:,}")
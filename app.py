"""
Streamlit UI App for Sentiment Analysis on Airbnb Reviews
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sentiment_analyzer import SentimentAnalyzer


def main():
    """Main function to run the Streamlit app."""
    
    # Page configuration
    st.set_page_config(
        page_title="Airbnb Reviews Sentiment Analysis",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and description
    st.title("🏠 Airbnb Reviews Sentiment Analysis")
    st.markdown("""
    This app analyzes the sentiment of Airbnb reviews using Natural Language Processing.
    You can either enter individual reviews or upload a CSV file with multiple reviews.
    """)
    
    # Initialize sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    # Sidebar for input method selection
    st.sidebar.header("Input Method")
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Single Review", "Multiple Reviews", "Upload CSV"]
    )
    
    # Main content area
    if input_method == "Single Review":
        handle_single_review(analyzer)
    elif input_method == "Multiple Reviews":
        handle_multiple_reviews(analyzer)
    else:
        handle_csv_upload(analyzer)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This app uses TextBlob for sentiment analysis. "
        "Polarity ranges from -1 (negative) to 1 (positive). "
        "Subjectivity ranges from 0 (objective) to 1 (subjective)."
    )


def handle_single_review(analyzer: SentimentAnalyzer):
    """Handle single review input and analysis."""
    st.header("📝 Analyze Single Review")
    
    # Text input
    review_text = st.text_area(
        "Enter an Airbnb review:",
        height=150,
        placeholder="Type or paste a review here..."
    )
    
    if st.button("Analyze Sentiment", type="primary"):
        if review_text.strip():
            with st.spinner("Analyzing sentiment..."):
                result = analyzer.analyze_sentiment(review_text)
            
            # Display results
            st.subheader("Analysis Results")
            
            # Create columns for metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                sentiment_emoji = {
                    "positive": "😊",
                    "negative": "😞",
                    "neutral": "😐"
                }
                st.metric(
                    "Sentiment",
                    f"{sentiment_emoji[result['sentiment']]} {result['sentiment'].capitalize()}"
                )
            
            with col2:
                polarity_color = "green" if result['polarity'] > 0 else "red" if result['polarity'] < 0 else "gray"
                st.metric("Polarity", f"{result['polarity']:.3f}")
            
            with col3:
                st.metric("Subjectivity", f"{result['subjectivity']:.3f}")
            
            # Visualization
            st.subheader("Sentiment Visualization")
            col1, col2 = st.columns(2)
            
            with col1:
                # Polarity gauge
                fig_polarity = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=result['polarity'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Polarity Score"},
                    gauge={
                        'axis': {'range': [-1, 1]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [-1, -0.1], 'color': "lightcoral"},
                            {'range': [-0.1, 0.1], 'color': "lightgray"},
                            {'range': [0.1, 1], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 0
                        }
                    }
                ))
                fig_polarity.update_layout(height=300)
                st.plotly_chart(fig_polarity, use_container_width=True)
            
            with col2:
                # Subjectivity gauge
                fig_subjectivity = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['subjectivity'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Subjectivity Score"},
                    gauge={
                        'axis': {'range': [0, 1]},
                        'bar': {'color': "darkorange"},
                        'steps': [
                            {'range': [0, 0.5], 'color': "lightyellow"},
                            {'range': [0.5, 1], 'color': "lightblue"}
                        ]
                    }
                ))
                fig_subjectivity.update_layout(height=300)
                st.plotly_chart(fig_subjectivity, use_container_width=True)
        else:
            st.warning("Please enter a review to analyze.")


def handle_multiple_reviews(analyzer: SentimentAnalyzer):
    """Handle multiple reviews input and batch analysis."""
    st.header("📋 Analyze Multiple Reviews")
    
    # Text area for multiple reviews
    st.markdown("Enter multiple reviews (one per line):")
    reviews_text = st.text_area(
        "Reviews:",
        height=250,
        placeholder="Paste multiple reviews here, one per line..."
    )
    
    if st.button("Analyze All Reviews", type="primary"):
        if reviews_text.strip():
            # Split by newlines and filter empty lines
            reviews = [r.strip() for r in reviews_text.split("\n") if r.strip()]
            
            if reviews:
                with st.spinner(f"Analyzing {len(reviews)} reviews..."):
                    df = analyzer.analyze_batch(reviews)
                
                display_batch_results(df, analyzer)
            else:
                st.warning("No valid reviews found.")
        else:
            st.warning("Please enter at least one review.")


def handle_csv_upload(analyzer: SentimentAnalyzer):
    """Handle CSV file upload and analysis."""
    st.header("📁 Upload CSV File")
    
    st.markdown("""
    Upload a CSV file with Airbnb reviews. The file should have a column named 'review' or 'text' containing the review text.
    """)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"File uploaded successfully! Found {len(df_upload)} rows.")
            
            # Display first few rows
            st.subheader("Preview of uploaded data")
            st.dataframe(df_upload.head(), use_container_width=True)
            
            # Identify review column
            review_column = None
            for col in ['review', 'text', 'comment', 'reviews', 'Review', 'Text', 'Comment']:
                if col in df_upload.columns:
                    review_column = col
                    break
            
            if review_column:
                st.info(f"Using column '{review_column}' for sentiment analysis.")
                
                if st.button("Analyze Reviews from CSV", type="primary"):
                    reviews = df_upload[review_column].dropna().astype(str).tolist()
                    
                    if reviews:
                        with st.spinner(f"Analyzing {len(reviews)} reviews..."):
                            df_results = analyzer.analyze_batch(reviews)
                        
                        display_batch_results(df_results, analyzer)
                    else:
                        st.warning("No valid reviews found in the selected column.")
            else:
                st.error("Could not find a review column. Please ensure your CSV has a column named 'review', 'text', or 'comment'.")
        
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")


def display_batch_results(df: pd.DataFrame, analyzer: SentimentAnalyzer):
    """Display results for batch analysis."""
    
    # Get statistics
    stats = analyzer.get_sentiment_stats(df)
    
    # Display statistics
    st.subheader("📊 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reviews", stats['total_reviews'])
    
    with col2:
        st.metric("Positive", f"{stats['positive']} ({stats['positive_percentage']:.1f}%)")
    
    with col3:
        st.metric("Neutral", f"{stats['neutral']} ({stats['neutral_percentage']:.1f}%)")
    
    with col4:
        st.metric("Negative", f"{stats['negative']} ({stats['negative_percentage']:.1f}%)")
    
    # Visualizations
    st.subheader("📈 Sentiment Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        sentiment_counts = df['sentiment'].value_counts()
        fig_pie = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Sentiment Distribution",
            color=sentiment_counts.index,
            color_discrete_map={
                'positive': '#90EE90',
                'neutral': '#D3D3D3',
                'negative': '#FFB6C6'
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart
        fig_bar = px.bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            title="Sentiment Counts",
            labels={'x': 'Sentiment', 'y': 'Count'},
            color=sentiment_counts.index,
            color_discrete_map={
                'positive': '#90EE90',
                'neutral': '#D3D3D3',
                'negative': '#FFB6C6'
            }
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Polarity distribution
    st.subheader("📉 Polarity Distribution")
    fig_hist = px.histogram(
        df,
        x='polarity',
        nbins=30,
        title="Distribution of Polarity Scores",
        labels={'polarity': 'Polarity Score', 'count': 'Frequency'},
        color_discrete_sequence=['#4169E1']
    )
    fig_hist.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Neutral")
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Scatter plot
    st.subheader("🔍 Polarity vs Subjectivity")
    fig_scatter = px.scatter(
        df,
        x='polarity',
        y='subjectivity',
        color='sentiment',
        title="Polarity vs Subjectivity",
        labels={'polarity': 'Polarity Score', 'subjectivity': 'Subjectivity Score'},
        color_discrete_map={
            'positive': '#90EE90',
            'neutral': '#D3D3D3',
            'negative': '#FFB6C6'
        },
        hover_data=['review']
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Display detailed results
    st.subheader("📄 Detailed Results")
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        sentiment_filter = st.multiselect(
            "Filter by sentiment:",
            options=['positive', 'neutral', 'negative'],
            default=['positive', 'neutral', 'negative']
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            options=['polarity', 'subjectivity', 'review_id'],
            index=0
        )
    
    # Filter and sort data
    filtered_df = df[df['sentiment'].isin(sentiment_filter)].sort_values(by=sort_by, ascending=False)
    
    # Display table
    st.dataframe(
        filtered_df[['review_id', 'review', 'sentiment', 'polarity', 'subjectivity']],
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="sentiment_analysis_results.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    main()

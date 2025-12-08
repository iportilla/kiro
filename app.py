"""
Kiro - Streamlit UI Application
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Kiro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🚀 Kiro")
st.markdown("Welcome to the Kiro example application built with Streamlit!")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select a page:",
        ["Home", "Data Visualization", "Interactive Demo", "About"]
    )
    
    st.markdown("---")
    st.markdown("### Settings")
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    st.info(f"Current theme: {theme}")

# Main content based on selected page
if page == "Home":
    st.header("Home")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Users", value="1,234", delta="123")
    
    with col2:
        st.metric(label="Active Sessions", value="456", delta="-12")
    
    with col3:
        st.metric(label="Response Time", value="45ms", delta="-5ms")
    
    st.markdown("---")
    
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.success("Data refreshed successfully!")
    
    with col2:
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("Report generation started...")
    
    with col3:
        if st.button("⚙️ Configure", use_container_width=True):
            st.warning("Configuration panel opening...")

elif page == "Data Visualization":
    st.header("Data Visualization")
    
    # Generate sample data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Series A', 'Series B', 'Series C']
    )
    
    st.subheader("Line Chart")
    st.line_chart(chart_data)
    
    st.subheader("Area Chart")
    st.area_chart(chart_data)
    
    st.subheader("Bar Chart")
    st.bar_chart(chart_data)
    
    # Data table
    st.subheader("Data Table")
    st.dataframe(chart_data, use_container_width=True)

elif page == "Interactive Demo":
    st.header("Interactive Demo")
    
    st.subheader("Input Controls")
    
    # Text input
    name = st.text_input("Enter your name:", "User")
    st.write(f"Hello, {name}! 👋")
    
    # Slider
    age = st.slider("Select your age:", 0, 100, 25)
    st.write(f"You selected: {age} years old")
    
    # Number input
    number = st.number_input("Pick a number:", min_value=0, max_value=100, value=50)
    st.write(f"Your number: {number}")
    
    # Date input
    date = st.date_input("Select a date:", datetime.now())
    st.write(f"Selected date: {date}")
    
    # Checkbox
    agree = st.checkbox("I agree to the terms and conditions")
    if agree:
        st.success("✅ Thank you for agreeing!")
    
    # Radio buttons
    option = st.radio(
        "Choose your favorite color:",
        ["Red", "Green", "Blue"]
    )
    st.write(f"You selected: {option}")
    
    # Select box
    city = st.selectbox(
        "Select your city:",
        ["New York", "London", "Tokyo", "Paris"]
    )
    st.write(f"You live in: {city}")
    
    # Multi-select
    options = st.multiselect(
        "What are your favorite programming languages?",
        ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
        ["Python"]
    )
    st.write(f"You selected: {', '.join(options)}")
    
    # File uploader
    st.subheader("File Upload")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size} bytes")

elif page == "About":
    st.header("About Kiro")
    
    st.markdown("""
    ## Overview
    
    Kiro is an example Streamlit application that demonstrates various features and capabilities.
    
    ### Features
    
    - **Interactive UI**: Built with Streamlit for rapid development
    - **Data Visualization**: Multiple chart types and data displays
    - **Responsive Design**: Works across different screen sizes
    - **Easy to Extend**: Simple Python code structure
    
    ### Technology Stack
    
    - **Frontend**: Streamlit
    - **Data Processing**: Pandas, NumPy
    - **Language**: Python 3.x
    
    ### Getting Started
    
    1. Install dependencies: `pip install -r requirements.txt`
    2. Run the application: `streamlit run app.py`
    3. Open your browser to the provided URL
    
    ### License
    
    MIT License - See LICENSE file for details
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Kiro © 2025 | Built with Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 🏠 Airbnb Sentiment Analyzer App Walkthrough

Welcome to the Airbnb Sentiment Analyzer! This application allows you to analyze the sentiment of Airbnb reviews using OpenAI's powerful language models.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- An OpenAI API Key

### Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the App

To start the application, run the following command in your terminal:

```bash
streamlit run app.py
```

This will open the app in your default web browser (usually at `http://localhost:8501`).

## 📖 Usage Guide

### 1. Configuration
On the left sidebar, you will find the **App Configuration** section.
- **OpenAI API Key**: Enter your OpenAI API key here. This is required for the app to function.
- **Model**: Select the model you want to use (`gpt-3.5-turbo` or `gpt-4`).

### 2. Input Methods
The app supports two ways to provide reviews for analysis:

#### A. Paste Text
1. Select "Paste Text" radio button.
2. Type or paste a single review into the text area.
3. Click "Run Analysis" in the sidebar.
4. View the Sentiment (Positive/Neutral/Negative), Score, and an Explanation.

#### B. Upload CSV
1. Select "Upload CSV" radio button.
2. Upload a CSV file containing a column named `comments`.
   - *Note: The app will process up to 20 reviews at a time for demonstration purposes.*
3. Click "Run Analysis" in the sidebar.
4. Watch the progress bar as reviews are analyzed.
5. View the results table and a sentiment distribution chart.

## 📂 Project Structure

- `app.py`: The main Streamlit application file.
- `sentiment_analysis.py`: Contains the core logic for interacting with OpenAI and processing sentiment.
- `requirements.txt`: List of Python dependencies.
- `test_sentiment.py`: Unit tests for the sentiment analysis logic.

## 🧪 Running Tests

To verify that the sentiment analysis logic is working correctly, you can run the included unit tests:

```bash
python3 test_sentiment.py
```

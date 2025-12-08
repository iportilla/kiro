# Kiro - Airbnb Reviews Sentiment Analysis

A Streamlit web application for analyzing sentiment in Airbnb reviews using Natural Language Processing.

## Features

- 📝 **Single Review Analysis**: Analyze individual reviews with detailed sentiment metrics
- 📋 **Batch Analysis**: Analyze multiple reviews at once
- 📁 **CSV Upload**: Upload CSV files with multiple reviews for bulk analysis
- 📊 **Interactive Visualizations**: Beautiful charts showing sentiment distribution, polarity, and subjectivity
- 📥 **Export Results**: Download analysis results as CSV files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/iportilla/kiro.git
cd kiro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download required NLTK data for TextBlob:
```bash
python -m textblob.download_corpora
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## How to Use

### Single Review Analysis
1. Select "Single Review" from the sidebar
2. Enter or paste a review in the text area
3. Click "Analyze Sentiment" to see results
4. View polarity and subjectivity scores with interactive gauges

### Multiple Reviews
1. Select "Multiple Reviews" from the sidebar
2. Enter multiple reviews (one per line)
3. Click "Analyze All Reviews"
4. View comprehensive statistics and visualizations

### CSV Upload
1. Select "Upload CSV" from the sidebar
2. Upload a CSV file with a 'review' or 'text' column
3. Preview your data
4. Click "Analyze Reviews from CSV"
5. Download results as CSV

## Sample Data

A sample CSV file (`sample_reviews.csv`) is included with 15 example Airbnb reviews for testing.

## Understanding the Metrics

- **Polarity**: Ranges from -1 (negative) to 1 (positive)
  - Positive: > 0.1
  - Neutral: -0.1 to 0.1
  - Negative: < -0.1

- **Subjectivity**: Ranges from 0 (objective) to 1 (subjective)
  - Objective statements are factual
  - Subjective statements express opinions or feelings

## Technologies Used

- **Streamlit**: Web application framework
- **TextBlob**: Natural Language Processing and sentiment analysis
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis

## License

MIT License - see LICENSE file for details

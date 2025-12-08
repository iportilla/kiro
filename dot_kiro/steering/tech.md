# Technology Stack

## Core Technologies

- **Language**: Python 3.11
- **Platform**: IBM Watson Machine Learning (WML) / watsonx.ai
- **Environment**: Jupyter Notebooks

## Key Libraries & Frameworks

- `ibm-watsonx-ai` - IBM Watson AI Python SDK for model deployment and inference
- `watson_nlp` - Watson Natural Language Processing library
- `pandas` - Data manipulation and CSV processing
- `scikit-learn` (v1.3.2) - Model evaluation and train/test splitting
- `wget` - Dataset downloading

## Models Used

- **Legal Sentiment**: `mistralai/mixtral-8x7b-instruct-v01` (foundation model via watsonx.ai)
- **Review Sentiment**: `targets-sentiment_transformer-workflow_multilingual_slate.153m.distilled-cpu` (Watson NLP pretrained model)

## Authentication & Setup

Projects require:
- IBM Cloud API key
- Watson Machine Learning instance
- Deployment space ID or project ID
- Service endpoint URL (region-specific)

## Common Workflows

### Running Notebooks
```bash
# Install dependencies
pip install -U ibm-watsonx-ai
pip install wget
pip install "scikit-learn==1.3.2"

# Launch Jupyter
jupyter notebook
```

### Model Deployment Pattern
1. Initialize WML client with credentials
2. Set default space/project
3. Store model/function to repository
4. Create online deployment
5. Score with test data

## Data Format

- **CSV files** with columns for text and sentiment labels
- Sentiment encoding: `-1` (negative), `0` (neutral), `1` (positive)

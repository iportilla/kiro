# Project Structure

## Directory Organization

```
.
├── legal/                          # Legal document sentiment analysis
│   ├── Legal_Sentences.csv         # Dataset: legal phrases with sentiment labels
│   └── Use watsonx, and `mixtral-8x7b-instruct-v01` to find sentiments of legal documents.ipynb
│
└── reviews/                        # Customer review sentiment analysis
    ├── Deploy_Pretrained_Sentiment_Model_Cloud.ipynb
    ├── berlin-2015-10-03-reviews.csv
    ├── london-2016-02-02-reviews.csv
    ├── new-york-city-2016-02-02-reviews.csv
    ├── paris-2015-09-02-reviews.csv
    └── san-francisco-2015-11-01-reviews.csv
```

## Folder Conventions

- **legal/** - Contains legal domain sentiment analysis using watsonx foundation models
- **reviews/** - Contains customer review sentiment analysis using Watson NLP pretrained models

## File Naming Patterns

- Notebooks use descriptive names indicating the model/service used
- CSV files follow pattern: `{location}-{date}-reviews.csv` for review data
- Legal data uses descriptive name: `Legal_Sentences.csv`

## Data Structure

All CSV files contain:
- Text/phrase column with content to analyze
- Sentiment column with numeric labels (-1, 0, 1)
- Optional ID column for tracking

## Notebook Structure

Both notebooks follow similar patterns:
1. Setup & authentication
2. Data loading
3. Model initialization/deployment
4. Prediction/scoring
5. Evaluation (optional)
6. Cleanup

When working with this codebase, maintain the separation between legal and review use cases in their respective directories.

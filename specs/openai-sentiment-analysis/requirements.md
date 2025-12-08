# Requirements Document

## Introduction

This specification defines a new sentiment analysis solution for Airbnb review comments using OpenAI's Large Language Models (LLMs). The solution will analyze customer reviews from various cities and predict sentiment (positive, neutral, negative) based on the comment text. This extends the existing sentiment analysis capabilities in the project by adding OpenAI as an alternative to IBM Watson services.

## Glossary

- **OpenAI LLM**: Large Language Model provided by OpenAI (e.g., GPT-4, GPT-3.5-turbo)
- **Sentiment**: The emotional tone of text, classified as positive (1), neutral (0), or negative (-1)
- **Review Dataset**: CSV files containing Airbnb listing reviews with comments and metadata
- **Jupyter Notebook**: Interactive Python environment for data analysis and model execution
- **API Key**: Authentication credential for accessing OpenAI services
- **Prompt Engineering**: The practice of crafting effective instructions for LLMs to achieve desired outputs

## Requirements

### Requirement 1: Data Loading and Preprocessing

**User Story:** As a data analyst, I want to load Airbnb review data from CSV files, so that I can prepare the comments for sentiment analysis.

#### Acceptance Criteria

1. WHEN the notebook is executed, THE system SHALL load review data from CSV files in the reviews directory
2. WHEN loading CSV data, THE system SHALL extract the comments column for sentiment analysis
3. WHEN preprocessing data, THE system SHALL handle missing or empty comments gracefully
4. WHEN data is loaded, THE system SHALL display sample records to verify data structure
5. WHERE multiple city datasets exist, THE system SHALL support loading data from any specified CSV file

### Requirement 2: OpenAI API Integration

**User Story:** As a developer, I want to integrate OpenAI's API into the notebook, so that I can use LLMs for sentiment prediction.

#### Acceptance Criteria

1. WHEN initializing the OpenAI client, THE system SHALL authenticate using a valid API key
2. WHEN the API key is required, THE system SHALL prompt the user securely without exposing the key in the notebook
3. WHEN selecting a model, THE system SHALL support configurable model selection (e.g., gpt-4, gpt-3.5-turbo)
4. WHEN API errors occur, THE system SHALL handle exceptions and provide meaningful error messages
5. WHEN making API calls, THE system SHALL implement rate limiting to avoid exceeding quota limits

### Requirement 3: Prompt Engineering for Sentiment Analysis

**User Story:** As a machine learning engineer, I want to design effective prompts for the LLM, so that sentiment predictions are accurate and consistent.

#### Acceptance Criteria

1. WHEN creating prompts, THE system SHALL include clear instructions for sentiment classification
2. WHEN defining output format, THE system SHALL specify that responses must be one of: -1, 0, or 1
3. WHEN providing examples, THE system SHALL use few-shot learning with representative samples from each sentiment class
4. WHEN processing reviews, THE system SHALL maintain consistent prompt structure across all predictions
5. WHERE ambiguous sentiment exists, THE system SHALL instruct the model to classify based on overall tone

### Requirement 4: Batch Sentiment Prediction

**User Story:** As a data analyst, I want to predict sentiment for multiple reviews efficiently, so that I can analyze large datasets.

#### Acceptance Criteria

1. WHEN processing reviews, THE system SHALL iterate through the dataset and predict sentiment for each comment
2. WHEN making predictions, THE system SHALL extract the sentiment label from the LLM response
3. WHEN batch processing, THE system SHALL display progress indicators for long-running operations
4. WHEN predictions complete, THE system SHALL store results in a structured format (DataFrame)
5. WHEN errors occur during prediction, THE system SHALL log the error and continue processing remaining reviews

### Requirement 5: Results Visualization and Analysis

**User Story:** As a data analyst, I want to visualize sentiment distribution and compare predictions, so that I can understand the sentiment patterns in the reviews.

#### Acceptance Criteria

1. WHEN predictions are complete, THE system SHALL display a summary of sentiment distribution (counts and percentages)
2. WHEN visualizing results, THE system SHALL create charts showing sentiment distribution
3. WHERE ground truth labels exist, THE system SHALL compare predicted vs actual sentiments
4. WHEN displaying results, THE system SHALL show sample predictions with original comments
5. WHEN analysis is complete, THE system SHALL calculate and display accuracy metrics if ground truth is available

### Requirement 6: Cost Tracking and Optimization

**User Story:** As a project manager, I want to track API usage and costs, so that I can manage the budget for sentiment analysis.

#### Acceptance Criteria

1. WHEN making API calls, THE system SHALL track the number of tokens used per request
2. WHEN batch processing completes, THE system SHALL display total tokens consumed
3. WHEN estimating costs, THE system SHALL calculate approximate API costs based on token usage
4. WHERE cost optimization is needed, THE system SHALL support sampling strategies to reduce API calls
5. WHEN processing large datasets, THE system SHALL provide options to limit the number of reviews analyzed

### Requirement 7: Export and Persistence

**User Story:** As a data analyst, I want to save sentiment predictions to a file, so that I can use the results in downstream analysis.

#### Acceptance Criteria

1. WHEN predictions are complete, THE system SHALL support exporting results to CSV format
2. WHEN exporting data, THE system SHALL include original review text, predicted sentiment, and metadata
3. WHEN saving results, THE system SHALL use descriptive filenames with timestamps
4. WHERE results already exist, THE system SHALL support loading previously saved predictions
5. WHEN exporting, THE system SHALL preserve the original data structure and add prediction columns

### Requirement 8: Notebook Documentation and Usability

**User Story:** As a new user, I want clear documentation and instructions in the notebook, so that I can understand and run the sentiment analysis workflow.

#### Acceptance Criteria

1. WHEN opening the notebook, THE system SHALL provide a clear introduction and overview
2. WHEN documenting code, THE system SHALL include markdown cells explaining each major section
3. WHEN requiring user input, THE system SHALL provide clear instructions and examples
4. WHEN displaying outputs, THE system SHALL format results in a readable and professional manner
5. WHEN the notebook completes, THE system SHALL provide a summary section with key findings and next steps

### Requirement 9: Error Handling and Robustness

**User Story:** As a developer, I want comprehensive error handling, so that the notebook can recover from common failures gracefully.

#### Acceptance Criteria

1. WHEN API rate limits are exceeded, THE system SHALL implement exponential backoff and retry logic
2. WHEN network errors occur, THE system SHALL catch exceptions and provide actionable error messages
3. WHEN invalid responses are received, THE system SHALL validate LLM outputs and handle parsing errors
4. WHEN file operations fail, THE system SHALL provide clear error messages about file paths and permissions
5. WHEN unexpected errors occur, THE system SHALL log the error details without crashing the entire notebook

### Requirement 10: Configuration and Flexibility

**User Story:** As a developer, I want configurable parameters, so that I can customize the sentiment analysis for different use cases.

#### Acceptance Criteria

1. WHEN initializing the notebook, THE system SHALL support configuration of model parameters (temperature, max_tokens)
2. WHEN selecting data, THE system SHALL allow users to specify which city dataset to analyze
3. WHEN processing reviews, THE system SHALL support limiting the number of reviews for testing purposes
4. WHERE different prompt strategies are needed, THE system SHALL support easy modification of the prompt template
5. WHEN running experiments, THE system SHALL support comparing results from different model configurations

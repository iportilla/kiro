# Implementation Plan

## Overview

This implementation plan breaks down the OpenAI sentiment analysis notebook into discrete, actionable tasks. Each task builds incrementally on previous work, with testing integrated throughout to ensure correctness.

---

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create new Jupyter notebook: `reviews/OpenAI_Sentiment_Analysis_Airbnb_Reviews.ipynb`
  - Add notebook header with title, description, and table of contents
  - Install required dependencies: `openai`, `pandas`, `numpy`, `matplotlib`, `python-dotenv`, `hypothesis`, `pytest`
  - Import all necessary libraries and configure logging
  - _Requirements: 8.1, 8.2_

- [x] 2. Implement Configuration Module
  - Create `Config` dataclass with all configuration parameters (API key, model name, temperature, max_tokens, batch_size, rate_limit_delay, file paths)
  - Add validation for configuration parameters
  - Implement secure API key input using `getpass` or environment variables
  - Add configuration display function (masking sensitive data)
  - _Requirements: 2.2, 10.1_

- [ ]* 2.1 Write property test for configuration validation
  - **Property 23: Parameter configuration effect**
  - **Validates: Requirements 10.1**

- [x] 3. Implement Data Loader Module
  - Create `ReviewDataLoader` class with `load_reviews()` method
  - Implement CSV loading with error handling for missing files
  - Add `extract_comments()` method to filter and extract comment column
  - Implement `validate_data()` to check for required columns
  - Add `get_sample()` method to display sample records
  - Handle missing/null values gracefully
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ]* 3.1 Write property test for comment extraction consistency
  - **Property 1: Comment extraction consistency**
  - **Validates: Requirements 1.2**

- [ ]* 3.2 Write property test for missing data handling
  - **Property 2: Missing data handling**
  - **Validates: Requirements 1.3**

- [ ]* 3.3 Write property test for multi-file loading
  - **Property 3: Multi-file loading support**
  - **Validates: Requirements 1.5**

- [x] 4. Implement Prompt Engine Module
  - Create `PromptEngine` class with prompt template
  - Implement `get_system_message()` with clear sentiment classification instructions
  - Create few-shot examples for positive, neutral, and negative sentiments
  - Implement `build_prompt()` to construct complete prompts
  - Add `validate_response()` to check if response is valid sentiment label (-1, 0, 1)
  - Make prompt template easily customizable
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 10.4_

- [ ]* 4.1 Write property test for prompt structure consistency
  - **Property 7: Prompt structure consistency**
  - **Validates: Requirements 3.4**

- [ ]* 4.2 Write property test for prompt template customization
  - **Property 25: Prompt template customization**
  - **Validates: Requirements 10.4**

- [x] 5. Implement OpenAI Client Wrapper
  - Create `OpenAIClient` class with initialization using API key and model name
  - Implement `predict_sentiment()` for single comment prediction
  - Add `_parse_response()` to extract sentiment and token counts from API response
  - Implement response validation to ensure sentiment is -1, 0, or 1
  - Add error handling for invalid responses (default to neutral with warning)
  - _Requirements: 2.1, 2.3, 4.2, 9.3_

- [ ]* 5.1 Write property test for model configuration flexibility
  - **Property 4: Model configuration flexibility**
  - **Validates: Requirements 2.3**

- [ ]* 5.2 Write property test for sentiment extraction validity
  - **Property 9: Sentiment extraction validity**
  - **Validates: Requirements 4.2**

- [x] 6. Implement rate limiting and retry logic
  - Add `_handle_rate_limit()` method with exponential backoff
  - Implement retry logic for rate limit errors (429)
  - Add configurable max retries and backoff factor
  - Implement rate limit delay between requests
  - Add retry logic for server errors (5xx) and network errors
  - Log all retry attempts with details
  - _Requirements: 2.5, 9.1, 9.2_

- [ ]* 6.1 Write property test for rate limiting enforcement
  - **Property 6: Rate limiting enforcement**
  - **Validates: Requirements 2.5**

- [ ]* 6.2 Write property test for exponential backoff behavior
  - **Property 21: Exponential backoff behavior**
  - **Validates: Requirements 9.1**

- [ ]* 6.3 Write property test for exception handling completeness
  - **Property 22: Exception handling completeness**
  - **Validates: Requirements 9.2, 9.3, 9.4, 9.5**

- [x] 7. Implement batch prediction functionality
  - Add `batch_predict()` method to process multiple comments
  - Implement progress tracking for batch processing
  - Add error resilience to continue processing after individual failures
  - Store all results including errors in structured format
  - Ensure all comments are processed (count matches input)
  - _Requirements: 4.1, 4.3, 4.4, 4.5_

- [ ]* 7.1 Write property test for complete batch processing
  - **Property 8: Complete batch processing**
  - **Validates: Requirements 4.1**

- [ ]* 7.2 Write property test for structured output format
  - **Property 10: Structured output format**
  - **Validates: Requirements 4.4**

- [ ]* 7.3 Write property test for error resilience
  - **Property 11: Error resilience**
  - **Validates: Requirements 4.5**

- [x] 8. Implement Cost Tracker Module
  - Create `CostTracker` class with model-specific pricing
  - Implement `add_request()` to record token usage per request
  - Add `get_total_tokens()` to return total input and output tokens
  - Implement `estimate_cost()` to calculate costs based on pricing
  - Create `display_summary()` to show usage and cost summary
  - _Requirements: 6.1, 6.2, 6.3_

- [ ]* 8.1 Write property test for token tracking accuracy
  - **Property 14: Token tracking accuracy**
  - **Validates: Requirements 6.1**

- [ ]* 8.2 Write property test for token aggregation
  - **Property 15: Token aggregation**
  - **Validates: Requirements 6.2**

- [ ]* 8.3 Write property test for cost calculation validity
  - **Property 16: Cost calculation validity**
  - **Validates: Requirements 6.3**

- [x] 9. Implement Prediction Pipeline
  - Create `SentimentPipeline` class to orchestrate the workflow
  - Implement `run()` method that coordinates all components
  - Add `_process_batch()` for batch processing with rate limiting
  - Implement `_aggregate_results()` to combine predictions into DataFrame
  - Integrate Cost Tracker to monitor token usage
  - Add support for limiting number of reviews processed
  - _Requirements: 6.4, 6.5, 10.3_

- [ ]* 9.1 Write property test for sampling effectiveness
  - **Property 17: Sampling effectiveness**
  - **Validates: Requirements 6.4, 6.5, 10.3**

- [x] 10. Checkpoint - Ensure all tests pass
  - Run all property-based tests
  - Verify data loading works with sample CSV
  - Test API integration with a few sample comments
  - Verify cost tracking is accurate
  - Ensure all error handling works correctly
  - Ask the user if questions arise

- [x] 11. Implement Results Analyzer Module
  - Create `ResultsAnalyzer` class
  - Implement `compute_distribution()` to calculate sentiment counts
  - Add `calculate_metrics()` for accuracy, precision, recall (if ground truth available)
  - Implement `plot_distribution()` to create bar charts
  - Add `display_samples()` to show sample predictions with original text
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 11.1 Write property test for distribution calculation
  - **Property 12: Distribution calculation**
  - **Validates: Requirements 5.1**

- [ ]* 11.2 Write property test for accuracy computation
  - **Property 13: Accuracy computation**
  - **Validates: Requirements 5.3, 5.5**

- [x] 12. Implement export and persistence functionality
  - Add `export_results()` method to save results to CSV
  - Implement descriptive filename generation with timestamps
  - Add functionality to load previously saved predictions
  - Ensure all original columns plus predictions are preserved
  - Verify round-trip integrity (save and load produces equivalent data)
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 12.1 Write property test for export data preservation
  - **Property 18: Export data preservation**
  - **Validates: Requirements 7.2, 7.5**

- [ ]* 12.2 Write property test for filename timestamp uniqueness
  - **Property 19: Filename timestamp uniqueness**
  - **Validates: Requirements 7.3**

- [ ]* 12.3 Write property test for round-trip data integrity
  - **Property 20: Round-trip data integrity**
  - **Validates: Requirements 7.4**

- [x] 13. Create main execution workflow in notebook
  - Add markdown cells explaining each section
  - Implement step-by-step workflow: Config → Load → Predict → Analyze → Export
  - Add data exploration section showing sample reviews
  - Include prompt testing section with example predictions
  - Add visualization section with charts
  - Include cost summary at the end
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 14. Add comprehensive error handling and logging
  - Configure logging to file and console
  - Add try-catch blocks around all major operations
  - Implement graceful degradation for non-critical errors
  - Add informative error messages with remediation steps
  - Log all API errors with details
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 15. Implement dataset selection flexibility
  - Add configuration option to select different city datasets
  - Create helper function to list available CSV files
  - Add validation for file existence
  - Support loading any CSV file from reviews directory
  - _Requirements: 10.2_

- [ ]* 15.1 Write property test for dataset selection flexibility
  - **Property 24: Dataset selection flexibility**
  - **Validates: Requirements 10.2**

- [x] 16. Add documentation and usage examples
  - Create comprehensive introduction section
  - Add prerequisites and setup instructions
  - Include example usage with different configurations
  - Document all configuration parameters
  - Add troubleshooting section for common issues
  - Include best practices for cost optimization
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 17. Create example analysis with real data
  - Load a sample of Paris reviews (limit to 50 for testing)
  - Run sentiment prediction
  - Display sentiment distribution
  - Show sample predictions with original comments
  - Export results to CSV
  - Display cost summary
  - _Requirements: All requirements integrated_

- [x] 18. Add comparison with ground truth (optional enhancement)
  - If ground truth labels are available, load them
  - Compare predicted vs actual sentiments
  - Calculate accuracy, precision, recall, F1 score
  - Create confusion matrix visualization
  - Analyze misclassified examples
  - _Requirements: 5.3, 5.5_

- [x] 19. Implement multi-model comparison (optional enhancement)
  - Add support for running predictions with multiple models (gpt-4, gpt-3.5-turbo)
  - Compare results across models
  - Compare costs across models
  - Create comparison visualizations
  - _Requirements: 10.5_

- [x] 20. Final checkpoint - Ensure all tests pass
  - Run complete test suite
  - Verify notebook executes end-to-end without errors
  - Test with different city datasets
  - Verify all visualizations render correctly
  - Confirm cost tracking is accurate
  - Validate exported CSV files
  - Ask the user if questions arise

- [x] 21. Add summary and next steps section
  - Summarize key findings from example analysis
  - Document total costs and token usage
  - Provide recommendations for production use
  - List potential improvements and extensions
  - Add references and resources
  - _Requirements: 8.5_

---

## Notes

- Tasks marked with `*` are optional testing tasks that can be skipped for faster MVP development
- Property-based tests use the `hypothesis` library with minimum 100 iterations
- Each property test is tagged with the format: `Feature: openai-sentiment-analysis, Property {number}: {property_text}`
- Checkpoint tasks ensure stability before proceeding to next phase
- The notebook should be executable from top to bottom without errors
- All API calls should be wrapped in error handling
- Cost tracking should be visible throughout execution

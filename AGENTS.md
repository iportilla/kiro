# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Build/Test Commands

**Run Streamlit app** (must be from code/ directory):
```bash
cd code && streamlit run app.py
```

**Run Chainlit app** (must be from code/ directory):
```bash
cd code && chainlit run chainlit_app.py
```

**Run tests** (uses unittest, not pytest):
```bash
cd code && python3 test_sentiment.py
```

## Critical Non-Obvious Patterns

**Directory structure has TWO code locations**:
- `code/` - Two UIs using OpenAI: Streamlit (app.py) and Chainlit (chainlit_app.py)
- `data/reviews/` and `data/legal/` - Jupyter notebooks using IBM Watson

**Two UI frameworks available**:
- Streamlit (app.py) - Dashboard/form-based, best for batch processing
- Chainlit (chainlit_app.py) - Chat-based, best for single reviews

**CSV files MUST have `comments` column** - Not `review`, `text`, or `comment` (singular)

**Streamlit app hardcodes 20 review limit** - See app.py line 86-88, intentional demo constraint

**Config class uses `__post_init__` validation** - Dataclass pattern with custom validation in _validate()

**API retry logic is custom-built** - Not using tenacity or backoff libraries, implements exponential backoff manually in OpenAIClient._calculate_backoff()

**Prompt structure is critical for accuracy**:
- System message defines task
- Few-shot examples (3 examples: positive/neutral/negative)
- User comment
- Must maintain this exact structure in PromptEngine.build_prompt()

**Response parsing has fallback logic** - See sentiment_analysis.py lines 182-189, handles chatty model responses

**Project uses Kiro spec-driven development** - Specs in `dot_kiro/specs/` (note: folder is `dot_kiro` not `.kiro`)

**Two sentiment analysis implementations**:
- OpenAI approach: code/sentiment_analysis.py (LLM-based)
- IBM Watson approach: data/*/notebooks (pretrained model-based)

**Rate limiting is enforced per-request** - 0.5s delay between API calls, configurable in Config.rate_limit_delay
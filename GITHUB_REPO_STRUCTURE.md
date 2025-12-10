# GitHub Repository Structure Guide

This document provides the recommended folder structure for pushing this project to GitHub.

---

## 📁 Recommended Repository Structure

```
airbnb-sentiment-analyzer/
│
├── .github/                          # GitHub-specific files
│   ├── workflows/                    # GitHub Actions (optional)
│   │   └── tests.yml                # Automated testing
│   └── ISSUE_TEMPLATE/              # Issue templates (optional)
│
├── .bob/                            # Bob IDE configuration
│   ├── rules-code/
│   │   └── AGENTS.md
│   ├── rules-advance/
│   │   └── AGENTS.md
│   ├── rules-ask/
│   │   └── AGENTS.md
│   └── rules-architect/
│       └── AGENTS.md
│
├── code/                            # Application source code
│   ├── .chainlit/                   # Chainlit configuration
│   │   ├── config.toml
│   │   └── README.md
│   │
│   ├── app.py                       # Streamlit original UI
│   ├── app_simple.py               # Streamlit simplified UI
│   ├── chainlit_app.py             # Chainlit chat UI
│   ├── sentiment_analysis.py       # Core backend logic
│   ├── test_sentiment.py           # Unit tests
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── QUICKSTART.md               # Quick start guide
│   ├── README_UI_COMPARISON.md     # UI comparison
│   ├── STREAMLIT_VERSIONS.md       # Streamlit versions
│   ├── UI_IMPLEMENTATION_SUMMARY.md # Implementation summary
│   └── APP_WALKTHROUGH.md          # Detailed walkthrough
│
├── data/                            # Sample datasets
│   ├── reviews/                     # Review datasets
│   │   ├── berlin-2015-10-03-reviews.csv
│   │   ├── paris-2015-09-02-reviews.csv
│   │   └── README.md               # Dataset documentation
│   │
│   └── legal/                       # Legal datasets
│       ├── Legal_Sentences.csv
│       └── README.md
│
├── docs/                            # Additional documentation (optional)
│   ├── images/                      # Screenshots, diagrams
│   └── examples/                    # Usage examples
│
├── tests/                           # Additional tests (optional)
│   └── integration/                 # Integration tests
│
├── .gitignore                       # Git ignore file
├── .env.example                     # Example environment variables
├── LICENSE                          # License file
├── README.md                        # Main project README
├── BOB_IDE_GUIDE.md                # Bob IDE guide
├── AGENTS.md                        # Main Bob rules
├── GITHUB_REPO_STRUCTURE.md        # This file
├── CONTRIBUTING.md                  # Contribution guidelines (optional)
└── requirements.txt                 # Root-level requirements (optional)
```

---

## 📝 Essential Files to Create

### 1. .gitignore

Create `.gitignore` in project root:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
*.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Jupyter Notebook
.ipynb_checkpoints

# Streamlit
.streamlit/

# Chainlit
.chainlit/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
```

### 2. .env.example

Create `.env.example` in project root:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model Configuration
DEFAULT_MODEL=gpt-3.5-turbo

# Optional: Rate Limiting
RATE_LIMIT_DELAY=0.5
MAX_RETRIES=3
```

### 3. LICENSE

Choose an appropriate license (MIT, Apache 2.0, etc.)

Example MIT License:
```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

### 4. Main README.md

Update the root `README.md` with:

```markdown
# Airbnb Sentiment Analyzer

Analyze sentiment in Airbnb reviews using OpenAI's language models with three different UI options.

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/airbnb-sentiment-analyzer.git
cd airbnb-sentiment-analyzer

# Install dependencies
cd code
pip install -r requirements.txt

# Set up API key
cp ../.env.example ../.env
# Edit .env and add your OpenAI API key

# Run your preferred UI
streamlit run app_simple.py  # Recommended
```

## 📚 Documentation

- [Quick Start Guide](code/QUICKSTART.md)
- [UI Comparison](code/README_UI_COMPARISON.md)
- [Bob IDE Guide](BOB_IDE_GUIDE.md)

## 🎨 Three UI Options

1. **Streamlit Simplified** - Fast, auto-run, production-ready
2. **Streamlit Original** - Comprehensive dashboard
3. **Chainlit** - Conversational chat interface

See [UI Comparison](code/README_UI_COMPARISON.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) file
```

### 5. CONTRIBUTING.md (Optional)

```markdown
# Contributing Guidelines

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update documentation
5. Submit a pull request

## Code Style

- Follow PEP 8 for Python code
- Add docstrings to functions
- Update AGENTS.md if adding non-obvious patterns
- Include tests for new features

## Testing

```bash
cd code
python3 test_sentiment.py
```
```

---

## 🚫 What NOT to Push to GitHub

### Sensitive Files
- `.env` - Contains API keys
- `*.log` - Log files
- `.streamlit/secrets.toml` - Streamlit secrets

### Generated Files
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python
- `.pytest_cache/` - Test cache

### IDE Files
- `.vscode/` - VS Code settings
- `.idea/` - PyCharm settings

### Large Files
- Consider using Git LFS for large datasets
- Or provide download links instead

---

## 📦 Preparing for GitHub

### Step 1: Clean Up

```bash
# Remove sensitive data
rm .env
rm -rf __pycache__
rm -rf .pytest_cache

# Create .env.example
cp .env .env.example
# Edit .env.example to remove actual keys
```

### Step 2: Create .gitignore

```bash
# Copy the .gitignore content from above
nano .gitignore
```

### Step 3: Initialize Git

```bash
# Initialize repository
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Airbnb Sentiment Analyzer with 3 UIs"
```

### Step 4: Create GitHub Repository

1. Go to GitHub.com
2. Click "New Repository"
3. Name: `airbnb-sentiment-analyzer`
4. Description: "Analyze Airbnb reviews with OpenAI - 3 UI options"
5. Choose Public or Private
6. Don't initialize with README (we have one)

### Step 5: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/yourusername/airbnb-sentiment-analyzer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🏷️ Recommended GitHub Topics

Add these topics to your repository for discoverability:

- `sentiment-analysis`
- `openai`
- `streamlit`
- `chainlit`
- `nlp`
- `airbnb`
- `python`
- `machine-learning`
- `ui`
- `bob-ide`

---

## 📋 GitHub Repository Settings

### Description
```
Analyze Airbnb review sentiment using OpenAI with 3 UI options: Streamlit (2 versions) and Chainlit. Built with Bob IDE.
```

### Website
Link to deployed app (if applicable)

### Topics
Add the topics listed above

### Features to Enable
- ✅ Issues
- ✅ Discussions (optional)
- ✅ Wiki (optional)
- ✅ Projects (optional)

---

## 🔒 Security Best Practices

### 1. Never Commit API Keys
```bash
# Check before committing
git diff

# If you accidentally committed a key:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

### 2. Use GitHub Secrets
For GitHub Actions, store secrets in:
- Settings → Secrets and variables → Actions

### 3. Add Security Policy
Create `SECURITY.md`:
```markdown
# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities to: security@example.com

Do not create public issues for security vulnerabilities.
```

---

## 📊 Optional: GitHub Actions

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        cd code
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd code
        python3 test_sentiment.py
```

---

## 📸 Add Screenshots

Create `docs/images/` and add:
- `streamlit-original.png`
- `streamlit-simplified.png`
- `chainlit-chat.png`

Reference in README:
```markdown
## Screenshots

### Streamlit Simplified
![Streamlit Simplified](docs/images/streamlit-simplified.png)

### Chainlit Chat
![Chainlit](docs/images/chainlit-chat.png)
```

---

## 🎯 Repository Checklist

Before pushing to GitHub:

- [ ] `.gitignore` created
- [ ] `.env.example` created (no real keys)
- [ ] `LICENSE` file added
- [ ] Main `README.md` updated
- [ ] All sensitive data removed
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Screenshots added (optional)
- [ ] GitHub Actions configured (optional)
- [ ] Repository description set
- [ ] Topics added

---

## 🌟 Making Your Repo Stand Out

### 1. Add Badges
```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://github.com/yourusername/repo/workflows/Tests/badge.svg)
```

### 2. Create a Demo
- Deploy to Streamlit Cloud
- Record a demo video
- Add GIF showing usage

### 3. Write Good Commit Messages
```bash
git commit -m "feat: Add simplified Streamlit UI with session caching"
git commit -m "docs: Update UI comparison guide"
git commit -m "fix: Resolve CSV column name validation"
```

### 4. Use GitHub Releases
Tag versions:
```bash
git tag -a v1.0.0 -m "Initial release with 3 UIs"
git push origin v1.0.0
```

---

## 📚 Additional Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

*Ready to share your project with the world!* 🚀
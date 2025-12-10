# 🚀 Quick Start Guide

Get up and running with the Airbnb Sentiment Analyzer in minutes!

---

## 📋 Prerequisites

- **Python 3.8+** installed
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Terminal/Command Prompt** access

---

## ⚡ Installation (One-Time Setup)

```bash
# 1. Navigate to the code directory
cd code

# 2. Install all dependencies
pip install -r requirements.txt

# 3. (Optional) Set up environment variable
echo "OPENAI_API_KEY=your-key-here" > .env
```

That's it! You're ready to run either UI.

---

## 🎨 Option 1: Streamlit UI

### Two Versions Available

#### A. Original (Comprehensive)
```bash
streamlit run app.py
```
- All options visible
- Manual "Run" button
- Wide dashboard layout
- Best for: Teaching, demonstrations, seeing all options

#### B. Simplified (Recommended)
```bash
streamlit run app_simple.py
```
- Auto-run on input
- Centered, compact layout
- Session cost tracking
- Download results
- Best for: Production use, frequent analysis, performance

### Access
Open your browser to: **http://localhost:8501**

### Quick Usage (Simplified Version)
1. Enter your OpenAI API key (auto-validates)
2. Choose your model (gpt-3.5-turbo or gpt-4)
3. Either:
   - **Paste a review** (analyzes automatically), OR
   - **Upload CSV** and click "Analyze All"
4. View results instantly
5. Download batch results if needed

### Best For
- Quick, frequent analysis
- Batch processing with visualizations
- Downloading results
- Performance-focused workflows

---

## 💬 Option 2: Chainlit UI (Chat Style)

### Start the App
```bash
chainlit run chainlit_app.py
```

### Access
Open your browser to: **http://localhost:8000**

### Quick Usage
1. Chat will ask for your OpenAI API key
2. Choose your model (type 1 or 2)
3. Either:
   - **Paste a review** directly in chat, OR
   - **Upload CSV** using the attachment button (📎)
4. Get instant results in conversational format
5. Type `cost` to see usage, `help` for commands

### Best For
- Quick single-review analysis
- Conversational, guided experience
- Mobile-friendly interface
- Natural language interaction

---

## 📊 Sample CSV Format

Both UIs require CSV files with a **`comments`** column:

```csv
listing_id,comments
123,"Amazing place! The host was super friendly and responsive."
456,"Decent location but the apartment was smaller than expected."
789,"Terrible experience. Place was dirty and host was rude."
```

**Important:** Column must be named `comments` (not `review`, `text`, etc.)

---

## 💰 Cost Estimates

### gpt-3.5-turbo (Recommended for testing)
- **Input:** $0.0015 per 1K tokens
- **Output:** $0.002 per 1K tokens
- **Typical review:** ~$0.001 - $0.003 per review

### gpt-4 (More accurate)
- **Input:** $0.03 per 1K tokens
- **Output:** $0.06 per 1K tokens
- **Typical review:** ~$0.02 - $0.05 per review

**Demo Limit:** Both UIs limit batch processing to 20 reviews to prevent unexpected costs.

---

## 🆘 Troubleshooting

### "Module not found" error
```bash
# Make sure you're in the code directory
cd code

# Reinstall dependencies
pip install -r requirements.txt
```

### "Invalid API key" error
- Check your API key is correct
- Ensure you have credits in your OpenAI account
- Try regenerating your API key

### Streamlit won't start
```bash
# Make sure you're in the code directory
cd code

# Try with full path
python -m streamlit run app.py
```

### Chainlit won't start
```bash
# Make sure you're in the code directory
cd code

# Try with full path
python -m chainlit run chainlit_app.py
```

### CSV upload fails
- Ensure CSV has a column named `comments`
- Check file is valid CSV format
- Try with a smaller file first (< 20 rows)

---

## 🎯 Which UI Should I Use?

### Use **Streamlit (Simplified)** if you:
- ✅ Need quick, frequent analysis
- ✅ Want auto-run on input
- ✅ Need to download batch results
- ✅ Want the best performance
- ✅ Prefer modern, streamlined UX

### Use **Streamlit (Original)** if you:
- ✅ Want all options visible at once
- ✅ Prefer manual execution control
- ✅ Need comprehensive dashboard view
- ✅ Teaching or demonstrating

### Use **Chainlit** if you:
- ✅ Analyze 1-5 reviews at a time
- ✅ Prefer conversational interfaces
- ✅ Use mobile devices frequently
- ✅ Want guided, step-by-step workflows

**Can't decide?** Try all three! They use the same backend, so you can switch anytime.

---

## 📚 Next Steps

### Learn More
- **Detailed Comparison:** See `README_UI_COMPARISON.md`
- **Streamlit Guide:** See `APP_WALKTHROUGH.md`
- **Backend Details:** See `sentiment_analysis.py` docstrings
- **Main README:** See `../README.md`

### Run Tests
```bash
cd code
python3 test_sentiment.py
```

### Explore the Code
- `app.py` - Streamlit UI (original)
- `app_simple.py` - Streamlit UI (simplified)
- `chainlit_app.py` - Chainlit UI
- `sentiment_analysis.py` - Shared backend logic
- `test_sentiment.py` - Unit tests

---

## 🎉 You're All Set!

Choose your preferred UI and start analyzing reviews:

```bash
# Streamlit Simplified (Recommended)
streamlit run app_simple.py

# OR Streamlit Original
streamlit run app.py

# OR Chainlit (Chat)
chainlit run chainlit_app.py
```

Happy analyzing! 🚀

---

## 💡 Pro Tips

1. **Start with gpt-3.5-turbo** - It's faster and cheaper for testing
2. **Test with single reviews first** - Before uploading large CSV files
3. **Monitor costs** - Both UIs show token usage and estimated costs
4. **Use .env file** - Store your API key to avoid re-entering it
5. **Try both UIs** - See which one fits your workflow better

---

*Need help? Check the troubleshooting section above or see the detailed documentation.*
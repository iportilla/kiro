"""
Chainlit-based Conversational UI for Airbnb Sentiment Analysis

This application provides a chat-based interface for analyzing sentiment in Airbnb reviews
using OpenAI's language models. It offers a conversational alternative to the Streamlit UI.
"""

import chainlit as cl
import pandas as pd
import os
from typing import Optional, Dict, Any, List
from sentiment_analysis import Config, PromptEngine, OpenAIClient, batch_predict

# Initialize global prompt engine (stateless)
prompt_engine = PromptEngine()

@cl.on_chat_start
async def start():
    """Initialize the chat session with welcome message and setup."""
    
    # Welcome message
    await cl.Message(
        content="""# 🏠 Welcome to Airbnb Sentiment Analyzer!

I'm your AI assistant for analyzing sentiment in Airbnb reviews. I can help you:

✨ **Analyze single reviews** - Paste any review and get instant sentiment analysis
📊 **Process CSV files** - Upload a CSV with multiple reviews for batch analysis
💰 **Track costs** - Monitor your OpenAI API usage and costs

To get started, I'll need your **OpenAI API key**. 

Please enter your API key (it will be stored securely in this session only):"""
    ).send()
    
    # Initialize session state
    cl.user_session.set("api_key", None)
    cl.user_session.set("config", None)
    cl.user_session.set("client", None)
    cl.user_session.set("total_cost", 0.0)
    cl.user_session.set("total_tokens", {"input": 0, "output": 0})
    cl.user_session.set("state", "awaiting_api_key")

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages and route to appropriate handler."""
    
    state = cl.user_session.get("state")
    
    # State machine for conversation flow
    if state == "awaiting_api_key":
        await handle_api_key(message.content)
    
    elif state == "awaiting_model_selection":
        await handle_model_selection(message.content)
    
    elif state == "ready":
        await handle_ready_state(message)
    
    elif state == "awaiting_review":
        await handle_single_review(message.content)
    
    else:
        await cl.Message(content="I'm not sure what to do. Let's start over. Type 'help' for options.").send()

async def handle_api_key(api_key: str):
    """Process and validate API key."""
    
    # Clean the API key
    api_key = api_key.strip()
    
    if not api_key or len(api_key) < 20:
        await cl.Message(
            content="❌ That doesn't look like a valid API key. Please enter your OpenAI API key:"
        ).send()
        return
    
    # Store API key
    cl.user_session.set("api_key", api_key)
    os.environ["OPENAI_API_KEY"] = api_key
    
    await cl.Message(
        content="""✅ API key received!

Now, which OpenAI model would you like to use?

1️⃣ **gpt-3.5-turbo** (Faster, cheaper - $0.0015 per 1K input tokens)
2️⃣ **gpt-4** (More accurate - $0.03 per 1K input tokens)

Type **1** or **2** to select:"""
    ).send()
    
    cl.user_session.set("state", "awaiting_model_selection")

async def handle_model_selection(selection: str):
    """Process model selection."""
    
    selection = selection.strip()
    
    if selection == "1":
        model_name = "gpt-3.5-turbo"
    elif selection == "2":
        model_name = "gpt-4"
    else:
        await cl.Message(
            content="❌ Please type **1** for gpt-3.5-turbo or **2** for gpt-4:"
        ).send()
        return
    
    # Initialize configuration and client
    api_key = cl.user_session.get("api_key")
    
    try:
        config = Config(api_key=api_key, model_name=model_name)
        client = OpenAIClient(api_key=api_key, model=model_name, config=config)
        
        cl.user_session.set("config", config)
        cl.user_session.set("client", client)
        cl.user_session.set("model_name", model_name)
        
        await cl.Message(
            content=f"""✅ Great! Using **{model_name}**

I'm ready to analyze reviews! What would you like to do?

📝 **Analyze a single review** - Just paste the review text
📊 **Upload CSV file** - Use the attachment button to upload a CSV with 'comments' column
💡 **Get help** - Type 'help' for more information
💰 **Check costs** - Type 'cost' to see your usage

What would you like to do?"""
        ).send()
        
        cl.user_session.set("state", "ready")
        
    except Exception as e:
        await cl.Message(
            content=f"❌ Error initializing: {str(e)}\n\nPlease check your API key and try again."
        ).send()
        cl.user_session.set("state", "awaiting_api_key")

async def handle_ready_state(message: cl.Message):
    """Handle messages when system is ready."""
    
    content = message.content.strip().lower()
    
    # Check for commands
    if content == "help":
        await show_help()
    elif content == "cost":
        await show_cost_summary()
    elif content == "reset":
        await reset_session()
    elif content.startswith("analyze"):
        await cl.Message(content="Please paste the review text you'd like to analyze:").send()
        cl.user_session.set("state", "awaiting_review")
    else:
        # Check if there are file attachments
        if message.elements:
            await handle_csv_upload(message.elements)
        else:
            # Treat as single review
            await handle_single_review(message.content)

async def handle_single_review(review_text: str):
    """Analyze a single review."""
    
    if not review_text or len(review_text.strip()) < 10:
        await cl.Message(
            content="⚠️ Please provide a review with at least 10 characters."
        ).send()
        cl.user_session.set("state", "ready")
        return
    
    client = cl.user_session.get("client")
    
    if not client:
        await cl.Message(content="❌ Client not initialized. Please restart.").send()
        return
    
    # Show processing message
    msg = cl.Message(content="🔄 Analyzing sentiment...")
    await msg.send()
    
    try:
        # Build prompt and predict
        messages = prompt_engine.build_prompt(review_text)
        result = client.predict_sentiment(review_text, messages)
        
        # Update cost tracking
        update_cost_tracking(result)
        
        # Format and display results
        if result.get("error"):
            await msg.update(content=f"❌ Error: {result['error']}")
        else:
            sentiment_emoji = {1: "😊", 0: "😐", -1: "😞"}
            sentiment_label = {1: "Positive", 0: "Neutral", -1: "Negative"}
            
            sentiment = result["sentiment"]
            
            response = f"""### Analysis Complete! {sentiment_emoji.get(sentiment, "🤔")}

**Review:** {review_text[:200]}{"..." if len(review_text) > 200 else ""}

**Sentiment:** {sentiment_label.get(sentiment, "Unknown")} ({sentiment})

**Explanation:** {result["explanation"]}

**Tokens Used:** {result["input_tokens"]} input + {result["output_tokens"]} output = {result["input_tokens"] + result["output_tokens"]} total

---

Would you like to analyze another review? Just paste it, or type 'cost' to see your total usage."""
            
            await msg.update(content=response)
        
        cl.user_session.set("state", "ready")
        
    except Exception as e:
        await msg.update(content=f"❌ Error during analysis: {str(e)}")
        cl.user_session.set("state", "ready")

async def handle_csv_upload(elements: List):
    """Handle CSV file upload and batch processing."""
    
    # Find CSV file
    csv_file = None
    for element in elements:
        if hasattr(element, 'path') and element.path.endswith('.csv'):
            csv_file = element
            break
    
    if not csv_file:
        await cl.Message(
            content="❌ Please upload a CSV file with a 'comments' column."
        ).send()
        return
    
    # Show processing message
    msg = cl.Message(content="📊 Processing CSV file...")
    await msg.send()
    
    try:
        # Load CSV
        df = pd.read_csv(csv_file.path)
        
        if 'comments' not in df.columns:
            await msg.update(
                content="❌ CSV must contain a 'comments' column. Found columns: " + ", ".join(df.columns)
            )
            return
        
        # Extract comments
        comments = df['comments'].dropna().astype(str).tolist()
        
        if len(comments) == 0:
            await msg.update(content="❌ No valid comments found in CSV.")
            return
        
        # Limit for demo
        if len(comments) > 20:
            await msg.update(
                content=f"⚠️ Found {len(comments)} reviews. Processing first 20 for demo purposes..."
            )
            comments = comments[:20]
        else:
            await msg.update(content=f"📊 Processing {len(comments)} reviews...")
        
        # Process batch
        client = cl.user_session.get("client")
        results = []
        
        for i, comment in enumerate(comments, 1):
            messages = prompt_engine.build_prompt(comment)
            result = client.predict_sentiment(comment, messages)
            results.append(result)
            update_cost_tracking(result)
            
            # Update progress
            if i % 5 == 0 or i == len(comments):
                await msg.update(content=f"📊 Processing... {i}/{len(comments)} reviews analyzed")
        
        # Create results summary
        results_df = pd.DataFrame(results)
        
        # Calculate distribution
        sentiment_counts = results_df['sentiment'].value_counts().to_dict()
        total = len(results_df)
        
        positive = sentiment_counts.get(1, 0)
        neutral = sentiment_counts.get(0, 0)
        negative = sentiment_counts.get(-1, 0)
        
        summary = f"""### ✅ Batch Analysis Complete!

**Total Reviews Analyzed:** {total}

**Sentiment Distribution:**
- 😊 Positive: {positive} ({positive/total*100:.1f}%)
- 😐 Neutral: {neutral} ({neutral/total*100:.1f}%)
- 😞 Negative: {negative} ({negative/total*100:.1f}%)

**Token Usage:**
- Total Input Tokens: {results_df['input_tokens'].sum()}
- Total Output Tokens: {results_df['output_tokens'].sum()}

**Sample Results:**
"""
        
        # Add sample results
        for idx, row in results_df.head(3).iterrows():
            sentiment_label = {1: "Positive", 0: "Neutral", -1: "Negative"}
            summary += f"\n{idx+1}. **{sentiment_label.get(row['sentiment'], 'Unknown')}**: {row['comment'][:100]}..."
        
        summary += "\n\n---\n\nType 'cost' to see total usage, or upload another CSV to continue."
        
        await msg.update(content=summary)
        
    except Exception as e:
        await msg.update(content=f"❌ Error processing CSV: {str(e)}")

async def show_help():
    """Display help information."""
    
    help_text = """### 📖 Help Guide

**Commands:**
- `help` - Show this help message
- `cost` - Display your API usage and costs
- `reset` - Start a new session

**Analyzing Reviews:**
- **Single Review:** Just paste the review text
- **Batch CSV:** Click the attachment button (📎) and upload a CSV file with a 'comments' column

**Tips:**
- Reviews should be at least 10 characters long
- CSV files are limited to 20 reviews for demo purposes
- Your API key is stored only for this session

What would you like to do next?"""
    
    await cl.Message(content=help_text).send()

async def show_cost_summary():
    """Display cost tracking summary."""
    
    total_cost = cl.user_session.get("total_cost", 0.0)
    total_tokens = cl.user_session.get("total_tokens", {"input": 0, "output": 0})
    model_name = cl.user_session.get("model_name", "unknown")
    
    summary = f"""### 💰 Cost Summary

**Model:** {model_name}

**Token Usage:**
- Input Tokens: {total_tokens['input']:,}
- Output Tokens: {total_tokens['output']:,}
- Total Tokens: {total_tokens['input'] + total_tokens['output']:,}

**Estimated Cost:** ${total_cost:.4f}

---

Ready to analyze more reviews?"""
    
    await cl.Message(content=summary).send()

async def reset_session():
    """Reset the session and start over."""
    
    cl.user_session.set("api_key", None)
    cl.user_session.set("config", None)
    cl.user_session.set("client", None)
    cl.user_session.set("total_cost", 0.0)
    cl.user_session.set("total_tokens", {"input": 0, "output": 0})
    cl.user_session.set("state", "awaiting_api_key")
    
    await cl.Message(
        content="🔄 Session reset! Please enter your OpenAI API key to start:"
    ).send()

def update_cost_tracking(result: Dict[str, Any]):
    """Update session cost tracking."""
    
    if result.get("error"):
        return
    
    # Get current totals
    total_cost = cl.user_session.get("total_cost", 0.0)
    total_tokens = cl.user_session.get("total_tokens", {"input": 0, "output": 0})
    model_name = cl.user_session.get("model_name", "gpt-3.5-turbo")
    
    # Pricing per 1K tokens
    pricing = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
    }
    
    model_pricing = pricing.get(model_name, pricing["gpt-3.5-turbo"])
    
    # Calculate cost for this request
    input_cost = (result["input_tokens"] / 1000) * model_pricing["input"]
    output_cost = (result["output_tokens"] / 1000) * model_pricing["output"]
    request_cost = input_cost + output_cost
    
    # Update totals
    total_cost += request_cost
    total_tokens["input"] += result["input_tokens"]
    total_tokens["output"] += result["output_tokens"]
    
    # Store updated values
    cl.user_session.set("total_cost", total_cost)
    cl.user_session.set("total_tokens", total_tokens)

if __name__ == "__main__":
    # This is handled by chainlit CLI
    pass
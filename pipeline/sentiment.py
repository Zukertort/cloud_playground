import feedparser
import google.generativeai as genai
import os
from dotenv import load_dotenv
import random

load_dotenv()

def get_news(ticker):
    print(f"Fetching news for {ticker}...")
    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}"
    
    first_5_entries = []
    d = feedparser.parse(rss_url)

    for entry in d.entries[:5]:
        first_5_entries.append(entry.title)
    
    return first_5_entries

def get_sentiment(headlines, mock=False):
    if mock == True:
        return random.uniform(-1.0, 1.0)
    if not headlines: return 0.0
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("No API Key found.")
        return 0.0

    print("Querying Gemini...")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-lite-latest')
    
    prompt = f"""Analyze the financial sentiment of these news headlines: {headlines}.
    
    Determine a single aggregate sentiment score from -1.0 (Very Negative) to 1.0 (Very Positive).
    
    CRITICAL: Return ONLY the raw number. Do not use markdown (bold/italics). Do not write sentences."""
    
    response = model.generate_content(prompt)

    try:
        clean_text = response.text.strip().replace('*', '')
        return float(clean_text)
    except ValueError:
        print(f"Gemini output invalid: '{response.text}'")
        return 0.0

if __name__ == "__main__":
    ticker = "AAPL"
    news = get_news(ticker)
    print(f"Headlines: {news}")
    
    if news:
        score = get_sentiment(news, mock=True)
        print(f"Sentiment Score: {score}")
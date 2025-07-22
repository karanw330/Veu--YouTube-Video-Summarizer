# 📺 Veu - YouTube Video Summarizer

**Veu** is a Flask-based web app that summarizes YouTube videos.  
Provide a YouTube URL — Veu scrapes the transcript, summarizes it using Google's **Gemini 2.5 Flash API**, and returns a markdown-formatted summary.

---

## 🚀 Features
- Auto-detects YouTube URLs.
- Scrapes transcripts from YouTube using **Selenium + BeautifulSoup**.
- Summarizes the transcript via **Gemini 2.5 Flash**.
- Supports general text queries with direct AI responses.
- Markdown-formatted responses.

---

## 🛠 Tech Stack
- **Flask** - Web server
- **Selenium** - Browser automation (headless Chrome)
- **BeautifulSoup** - HTML parsing
- **google-generativeai** - Gemini AI SDK
- **Markdown** - For formatting
- **ChromeDriver** - For Selenium

---

## ✅ Prerequisites
- Python 3.8+
- Google Gemini API Key
- Google Chrome installed
- ChromeDriver installed (matching Chrome version)

---

## 📦 Installation

```bash
pip install flask selenium beautifulsoup4 google-generativeai markdown
```

---

## Configuration
- Create a file named: **secret_data.py**
- Inside secret_data.py, add: **googleapi_key = "YOUR_GOOGLE_API_KEY"**
- Replace "YOUR_GOOGLE_API_KEY" with your actual Gemini API key.

---

## 💡 Usage
- ▶️ Summarizing a YouTube Video
- Paste a YouTube video URL.
  
The app scrapes the transcript using Selenium, sends the transcript to Gemini for summarization, displays the formatted summary.

## 💬 For Text Queries
Input any text query.
Gemini responds directly.

---

## ⚠️ Important Notes
- ChromeDriver must match your Chrome version.
- YouTube UI changes might break scraping — XPaths may need updates.
- Selenium runs in headless mode — remove the headless flag for debugging.




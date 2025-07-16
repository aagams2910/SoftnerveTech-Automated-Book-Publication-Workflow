# Automated Book Workflow

Automates scraping, AI rewriting, human review, version control, and RL-based optimization for book chapters.

## Features
- Scrape chapter content and screenshots from a URL
- Rewrite and review using Google Gemini
- Human-in-the-loop Streamlit UI
- Version control and semantic search with ChromaDB
- RL reward engine for feedback-driven improvement
- (Optional) Voice input/output

## Setup
1. Clone the repo and `cd` into the directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
3. Set your Google Gemini API key as an environment variable:
   ```bash
   export GEMINI_API_KEY=your_key_here  # or set in your OS-specific way
   ```

## Directory Structure
```
automated_book_workflow/
├── scraper/
│   └── playwright_scraper.py
├── ai_agents/
│   ├── writer.py
│   └── reviewer.py
├── rl_engine/
│   └── reward_model.py
├── interface/
│   └── streamlit_review.py
├── db/
│   └── chroma_utils.py
├── main.py
├── requirements.txt
└── README.md
output/  # stores scraped text and screenshots
```

## Test Run
Run the workflow on the sample URL:
```
python main.py --url "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
```

## Notes
- Requires a valid Google Gemini API key.
- For voice features, ensure your system has a microphone and speakers.

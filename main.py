import argparse
import os
from dotenv import load_dotenv
from automated_book_workflow.scraper.playwright_scraper import scrape_chapter
from automated_book_workflow.ai_agents.writer import rewrite_chapter
from automated_book_workflow.ai_agents.reviewer import review_chapter
from automated_book_workflow.rl_engine.reward_model import compute_reward, update_prompt_with_reward
from automated_book_workflow.db.chroma_utils import save_version
import streamlit as st
import sys

load_dotenv()

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main_workflow(url, output_dir='output'):
    print(f"[Main] Scraping chapter from {url}")
    text_path, screenshot_path = scrape_chapter(url, output_dir)
    original_text = read_file(text_path)
    print(f"[Main] Scraped text saved to {text_path}, screenshot to {screenshot_path}")

    ai_text = rewrite_chapter(original_text)
    print("[Main] AI-spun text generated.")

    review = review_chapter(ai_text)
    reviewed_text = ai_text
    print(f"[Main] Review: {review}")

    reward = compute_reward("accept", review.get("score", 0.5))
    print(f"[Main] Initial RL reward: {reward}")

    version_history = []
    metadata = {"feedback": "initial", "comments": review.get("comments", "")}
    version_id = save_version(reviewed_text, metadata)
    version_history.append({"id": version_id, "text": reviewed_text, "metadata": metadata})

    from automated_book_workflow.interface import streamlit_review
    streamlit_review.main(original_text, ai_text, reviewed_text, version_history)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Book Workflow")
    parser.add_argument('--url', type=str, required=True, help='URL of the chapter to process')
    args = parser.parse_args()
    main_workflow(args.url)

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("Warning: GEMINI_API_KEY not set. Please add it to your .env file.") 
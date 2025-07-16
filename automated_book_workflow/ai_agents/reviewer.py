import os
import google.generativeai as genai
import re
import json

def extract_json_from_response(text):
    code_block = re.search(r'```(?:json)?\s*([\s\S]+?)\s*```', text)
    if code_block:
        json_str = code_block.group(1)
    else:
        json_str = text
    brace_block = re.search(r'\{[\s\S]+\}', json_str)
    if brace_block:
        json_str = brace_block.group(0)
    try:
        return json.loads(json_str)
    except Exception:
        return None

def review_chapter(rewritten_text: str) -> dict:
    """
    Use Gemini to review the rewritten chapter for quality, clarity, and engagement.
    Returns a dict with review results.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[Reviewer] Warning: GEMINI_API_KEY not set. Returning neutral review.")
        return {"score": 0.5, "comments": "No API key provided."}
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    prompt = (
        "Review the following rewritten book chapter for quality, clarity, and engagement. "
        "Give a score from 0 (poor) to 1 (excellent) and provide brief comments.\n\n" + rewritten_text +
        "\n\nRespond in JSON: {\"score\": <float>, \"comments\": <string>}"
    )
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        review = extract_json_from_response(text)
        if review and 'score' in review and 'comments' in review:
            return review
        elif text:
            return {"score": 0.5, "comments": text}
        else:
            return {"score": 0.5, "comments": "No response from Gemini."}
    except Exception as e:
        print(f"[Reviewer] Gemini API error: {e}")
        return {"score": 0.5, "comments": str(e)} 
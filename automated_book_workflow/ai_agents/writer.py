import os
import google.generativeai as genai

def rewrite_chapter(raw_text: str) -> str:
    """
    Use Gemini to creatively rewrite the chapter content.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[Writer] Warning: GEMINI_API_KEY not set. Returning original text.")
        return raw_text
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    prompt = (
        "Rewrite the following book chapter in a completely new way. "
        "Use different sentence structures, synonyms, and a more engaging, modern style. "
        "Do NOT copy any sentences verbatim from the original. Make it feel like a new author wrote it, but keep the meaning and story the same.\n\n"
        + raw_text
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Writer] Gemini API error: {e}")
        return raw_text 
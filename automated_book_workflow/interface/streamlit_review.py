import os
import sys
import streamlit as st
import pyttsx3
import speech_recognition as sr

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from automated_book_workflow.db.chroma_utils import save_version, semantic_search
from automated_book_workflow.rl_engine.reward_model import compute_reward

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for your feedback...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return ""

def main(original_text: str, ai_text: str, reviewed_text: str, version_history: list):
    """
    Streamlit UI for human-in-the-loop review.
    """
    st.title("Automated Book Workflow Review")
    st.header("Original Chapter")
    st.write(original_text)
    if st.button("Read Original Aloud"):
        speak(original_text)
    st.header("AI-Spun Chapter")
    st.write(ai_text)
    if st.button("Read AI Version Aloud"):
        speak(ai_text)
    st.header("Reviewed Chapter")
    st.write(reviewed_text)
    if st.button("Read Reviewed Aloud"):
        speak(reviewed_text)

    st.subheader("Your Feedback")
    feedback = st.radio("Accept or Reject this version?", ("accept", "reject"))
    comments = st.text_area("Comments (or use voice input below):")
    if st.button("Use Voice Input for Comments"):
        comments = listen()
        st.text_area("Comments (or use voice input below):", value=comments)

    if st.button("Submit Feedback"):
        st.success(f"Feedback submitted: {feedback}, Comments: {comments}")
        metadata = {"feedback": feedback, "comments": comments}
        save_version(reviewed_text, metadata)

    st.subheader("Semantic Search")
    query = st.text_input("Search previous versions:")
    if st.button("Search") and query:
        results = semantic_search(query)
        for r in results:
            st.markdown(f"**Score:** {r['score']:.2f}")
            st.write(r['text'])
            st.write(r['metadata'])

    st.subheader("Version History")
    for v in version_history:
        st.write(v)

if __name__ == "__main__":
    from automated_book_workflow.db.chroma_utils import collection
    try:
        results = collection.get()
        if results['documents']:
            latest_text = results['documents'][-1]
            latest_meta = results['metadatas'][-1]
            version_history = [
                {"id": i, "text": t, "metadata": m}
                for i, t, m in zip(results['ids'], results['documents'], results['metadatas'])
            ]
            main(latest_text, latest_text, latest_text, version_history)
        else:
            st.warning("No versions found in ChromaDB. Please run the main workflow first.")
    except Exception as e:
        st.error(f"Error loading data from ChromaDB: {e}") 
import streamlit as st
import openai
import json
import tempfile
import os
import time

# Set your OpenAI API Key
openai.api_key = "xxxxx"  # <-- Remember to replace with your real API key

# --- Streamlit App Setup ---
st.set_page_config(page_title="UNICC AI Media Analysis Tool", layout="wide")
st.title("🧠 UNICC AI Media Analysis Tool")
st.caption("Ethical AI-driven content moderation for text and future media formats - Capstone 2025")

st.markdown("---")

# Sidebar Upload
st.sidebar.header("📁 Upload Your Content")
file_type = st.sidebar.selectbox("Select File Type:", ["Text", "Audio", "Video"])
uploaded_file = st.sidebar.file_uploader("Upload a File", type=["txt", "mp3", "wav", "mp4"])

# Helper Function: Text Analysis
def analyze_text_content(text_content):
    system_prompt = """You are a multilingual content moderation expert. Detect if the following text includes any of the following: xenophobic speech, hate speech, misinformation, or harmful/dehumanizing narratives.
Respond ONLY in valid JSON format like this:
{
  "is_harmful": true/false,
  "category": "...",
  "confidence": 0.0 - 1.0,
  "reason": "..."
}"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_content}
            ],
            temperature=0
        )
        content = response["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return parsed
    except Exception as e:
        return {"error": str(e)}

# --- Tabs Layout ---
tab1, tab2 = st.tabs(["📝 Text Analysis", "🎥 Video Analysis"])

# --- Text Analysis Tab ---
with tab1:
    st.header("Text Analysis")
    st.markdown("Upload a `.txt` file and analyze it for xenophobic language, misinformation, and harmful narratives.")

    if file_type == "Text" and uploaded_file is not None:
        user_prompt = st.text_input("💬 Ask a Question About the Text (Optional):")

        if st.button("🔎 Analyze Text"):
            with st.spinner("Analyzing Text Content..."):
                text_content = uploaded_file.read().decode("utf-8")
                analysis_result = analyze_text_content(text_content)
                time.sleep(2)

            if "error" in analysis_result:
                st.error(f"❌ Error analyzing file: {analysis_result['error']}")
            else:
                st.success("✅ Text Analysis Complete!")
                st.metric(label="Detected Harmfulness", value="⚠️ Harmful" if analysis_result["is_harmful"] else "✅ Safe")
                st.metric(label="Category", value=analysis_result["category"])
                st.progress(analysis_result["confidence"])
                st.info(f"**Reason:** {analysis_result['reason']}")

                if user_prompt:
                    st.markdown("---")
                    st.subheader("🔎 Answer to Your Question")
                    st.info(f"'{user_prompt}' → Based on the analyzed content, {analysis_result['reason']}")

    elif file_type == "Text":
        st.warning("📄 Please upload a text file (.txt) first.")

# --- Video Analysis Tab ---
with tab2:
    st.header("Video Analysis (Coming Soon 🚀)")
    st.markdown("""
    📽️ Video upload and harmful content analysis is a future feature.
    Due to Streamlit Cloud limitations (Whisper model size and GPU needs), video/audio processing will be integrated via external APIs in later versions.
    """)
    st.info("For now, please use the Text Analysis tab above!")

# Footer
st.markdown("---")
st.caption("© 2025 UNICC Capstone • Developed with ❤️ by Bo Ji")



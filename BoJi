import streamlit as st
import openai
import whisper
import json
import tempfile
import os
import time

# Set OpenAI API Key
openai.api_key = "xxxxx"  # Replace with your real key

# Whisper model for video transcription
whisper_model = whisper.load_model("base")

# Page setup
st.set_page_config(page_title="UNICC AI Media Analysis Tool", layout="wide")

# Main Title
st.title("🧠 UNICC AI Media Analysis Tool")
st.caption("Ethical AI-driven content moderation for text, audio, and video - Capstone 2025")

st.markdown("---")

# Sidebar
st.sidebar.header("📁 Upload Your Content")
file_type = st.sidebar.selectbox("Select File Type:", ["Text", "Audio", "Video"])
uploaded_file = st.sidebar.file_uploader("Upload a File", type=["txt", "mp3", "wav", "mp4"])

# Helper Functions
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

def analyze_video_file(video_path):
    segments = whisper_model.transcribe(video_path)["segments"]
    harmful_count = 0
    total_segments = len(segments)
    detailed_results = []

    for seg in segments:
        text = seg['text']
        prompt = f"""
You are a content moderation AI. Given the following text from a video, decide if it contains hate speech, harmful language, or offensive content. Respond with "Harmful" or "Safe", and explain briefly why.

Text: "{text}"
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            result_text = response["choices"][0]["message"]["content"].strip()
            detailed_results.append((seg['start'], seg['end'], text, result_text))

            if "Harmful" in result_text:
                harmful_count += 1
        except Exception as e:
            detailed_results.append((seg['start'], seg['end'], text, f"Error: {e}"))

    toxicity_rate = (harmful_count / total_segments) * 100 if total_segments else 0
    return toxicity_rate, detailed_results

# Interactive Tabs
tab1, tab2 = st.tabs(["📝 Text Analysis", "🎥 Video Analysis"])

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

with tab2:
    st.header("Video Analysis")
    st.markdown("Upload a `.mp4` video file to transcribe and detect harmful content across segments.")

    if file_type == "Video" and uploaded_file is not None:
        if st.button("🎬 Analyze Video"):
            with st.spinner("Transcribing and analyzing video... (this might take a few minutes)"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                toxicity_rate, results = analyze_video_file(tmp_path)
                os.remove(tmp_path)
                time.sleep(2)

            st.success(f"✅ Video Analysis Complete! Toxicity Rate: {toxicity_rate:.2f}%")
            st.progress(toxicity_rate/100)

            for start, end, text, result in results:
                with st.expander(f"🕑 [{start:.2f}s - {end:.2f}s] Segment"):
                    st.code(text)
                    st.info(result)

    elif file_type == "Video":
        st.warning("🎥 Please upload a video file (.mp4) first.")

# Footer
st.markdown("---")
st.caption("© 2025 UNICC Capstone • Developed with ❤️ by Bo Ji")


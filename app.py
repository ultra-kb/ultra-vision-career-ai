
import openai
import streamlit as st
import tempfile
import os

# --- Branding ---
st.set_page_config(page_title="Ultra Vision Career Explorer", page_icon="🎓")
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/your-repo/ultra-logo.png' width='150'>
        <h1 style='color: #0A74DA;'>Ultra Vision Academy</h1>
        <h3><i>A Vision to make student dignified person</i></h3>
    </div>
    """, unsafe_allow_html=True
)

# --- Inputs ---
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

uploaded_audio = st.file_uploader("🎤 Upload Student Voice (MP3/WAV saying 'I want to be a ___')", type=["mp3", "wav"])
uploaded_image = st.file_uploader("📸 Upload Student Photo (optional, for display)", type=["jpg", "jpeg", "png"])

if uploaded_audio and openai_api_key:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        tmp_audio.write(uploaded_audio.read())
        tmp_audio_path = tmp_audio.name

    with open(tmp_audio_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f, api_key=openai_api_key)
    os.unlink(tmp_audio_path)

    command = transcript["text"]
    st.success(f"🗣 Transcribed: {command}")

    if "I want to be" in command:
        profession = command.split("I want to be")[-1].strip()
        prompt = f"A realistic photo of a child as a {profession}, smiling, in professional clothes, high quality, modern background"

        if uploaded_image:
            st.image(uploaded_image, caption="Student Photo", width=200)

        st.info(f"🎨 Generating: You as a {profession}...")

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
            api_key=openai_api_key
        )
        image_url = response['data'][0]['url']
        st.image(image_url, caption=f"AI Image: You as a {profession}")
    else:
        st.warning("⚠️ Please say something like: 'I want to be a doctor'")

# Footer
st.markdown(
    """<hr style='margin-top:50px;margin-bottom:20px;'>
    <div style='text-align: center; color: grey;'>
        Visit us at <a href='https://www.ultravisionschool.com' target='_blank'>www.ultravisionschool.com</a><br>
        &copy; 2025 Ultra Vision Academy. All rights reserved.
    </div>
    """, unsafe_allow_html=True
)

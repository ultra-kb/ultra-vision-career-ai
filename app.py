
import openai
import streamlit as st
import tempfile
import os

# --- Branding ---
st.set_page_config(page_title="Ultra Vision Mobile Career Explorer", page_icon="🎓")
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/your-repo/ultra-logo.png' width='120'>
        <h2 style='color: #0A74DA;'>Ultra Vision Academy</h2>
        <p><i>A Vision to make student dignified person</i></p>
    </div>
    """, unsafe_allow_html=True
)

# --- API Key Input ---
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# --- Webcam Photo Capture ---
photo = st.camera_input("📸 Take your photo")

# --- Microphone Recorder (HTML5 Recorder via st.components.v1.html) ---
st.markdown("### 🎤 Record your voice (say 'I want to be a ___')")

import streamlit.components.v1 as components

components.html('''
<div>
  <button onclick="startRecording()" style="padding:10px 20px;font-size:16px;">🎙️ Start Recording</button>
  <button onclick="stopRecording()" style="padding:10px 20px;font-size:16px;">⏹️ Stop</button>
  <p id="status"></p>
  <audio id="audioPlayback" controls style="margin-top:10px;"></audio>
  <script>
    let mediaRecorder;
    let audioChunks = [];

    function startRecording() {
      navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        audioChunks = [];
        mediaRecorder.ondataavailable = event => {
          audioChunks.push(event.data);
        };
        document.getElementById("status").innerText = "Recording...";
      });
    }

    function stopRecording() {
      mediaRecorder.stop();
      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunks, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(blob);
        const audio = document.getElementById("audioPlayback");
        audio.src = audioUrl;

        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function () {
          const base64data = reader.result;
          const pyInput = window.streamlitWebcamInput || {};
          pyInput['audio'] = base64data;
          window.parent.postMessage({ type: 'streamlit:setComponentValue', value: pyInput }, '*');
        };
        document.getElementById("status").innerText = "Recording stopped.";
      };
    }
  </script>
</div>
''', height=250)

# Manual text fallback for career input
manual_command = st.text_input("🧠 Or type what you said:", placeholder="I want to be a doctor")

if openai_api_key and manual_command and photo:
    if "I want to be" in manual_command:
        profession = manual_command.split("I want to be")[-1].strip()
        prompt = f"A realistic photo of a child as a {profession}, smiling, in professional clothes, high quality, modern background"

        st.image(photo, caption="Your Photo", width=200)
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
    """<hr>
    <div style='text-align: center; color: grey;'>
        Visit us at <a href='https://www.ultravisionschool.com' target='_blank'>www.ultravisionschool.com</a><br>
        &copy; 2025 Ultra Vision Academy
    </div>
    """, unsafe_allow_html=True
)

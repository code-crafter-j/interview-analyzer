from gpt import GptClient
from convertVideoToAudio import ConvertVideoToAudio
from transcribe import Transcribe

import streamlit as st
import logging
import sys
import os
import pandas as pd

gptClient = GptClient()
convertVideoToAudio = ConvertVideoToAudio()
transcribe = Transcribe()

directory = '/home/ubuntu/demo_data/interview'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

def is_actual_file(file_name):
    if file_name.startswith('.'):
        return False
    if file_name.endswith('~'):
        return False
    if file_name.endswith('.tmp'):
        return False
    return True

def main():
    st.markdown(
        """
        <style>
        .stApp {
            color:#FF9999
            background-color:#E4EED3;
        }
        .block-container {
            max-width: 90%;
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }
        .stSelectbox > div[role="listbox"] {
            width: 400px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    def set_selectbox_width(width: int):
        st.markdown(
            f"""
            <style>
            .stSelectbox div[data-baseweb="select"] {{
                width: {width}px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    st.title("Interview Analyzer")
    st.markdown("""
                For using this, you need to insert your video into the below path\n
                <span style="padding: 2px; font-family: monospace;">
                192.168.1.10\\_temp\\interview_analyzier
                </span>
                """, unsafe_allow_html=True)

    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))  and is_actual_file(f) and (f.lower().endswith('.mp4') or f.lower().endswith('.mp3'))]
    except FileNotFoundError:
        st.error("The directory does not exist. Please check the path.")
        files = []

    set_selectbox_width(400)
    selected_file = st.selectbox('Select a file', files)
    selected_lang = st.selectbox('Select a language', ['en_us', 'ja'])
    
    if selected_file and selected_lang:
        submitBtn = st.button('Analyze', disabled=False)
    else:
        submitBtn = st.button('Analyze', disabled=True)

    tab1, tab2 = st.tabs(["Summary", "Advanced"])

    if submitBtn:
        with st.spinner('Processing ...'):
            audio_path = convertVideoToAudio.video_to_audio(directory, selected_file)
            transcribeData = transcribe.transcribe_AAI(audio_path, selected_lang)
            transcribeStr = transcribe.format_transcription(transcribeData)
            try:
                response_summary = gptClient.get_response_summary(transcribeStr)
                response_advanced = gptClient.get_response_advanced(transcribeStr)

                with tab1:
                    st.markdown(response_summary)

                with tab2:
                    st.markdown(response_advanced)
                    
            except Exception as e:
                st.error(f'Parsing error: {e}')

if __name__ == "__main__":
    main()


import streamlit as st
from moviepy.editor import VideoFileClip
import os

class ConvertVideoToAudio():
    def video_to_audio(self, directory, selected_file):
        file_path = os.path.join(directory, selected_file)

        if selected_file.lower().endswith('.mp3'):
            return file_path
        try:
            audio_path = os.path.splitext(file_path)[0] + '.mp3'
            video_clip = VideoFileClip(file_path)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(audio_path)
            audio_clip.close()
            video_clip.close()
            return audio_path
        except:
            st.error('Error while convert video to audio')
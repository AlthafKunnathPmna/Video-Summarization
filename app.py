import os
import streamlit as st
from utils.summarization import process_video

def main():
    st.title("Video Summarization Tool")
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])
    summary_type = st.radio("Choose Summary Type:", ["Short Summary", "Structured Summary"])

    if st.button("Generate Summary"):
        if uploaded_file is not None:
            os.makedirs("uploads", exist_ok=True)
            video_path = f"uploads/{uploaded_file.name}"
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            progress_bar = st.progress(0)
            summary_path = process_video(video_path, summary_type, progress_bar)

            with open(summary_path, "rb") as f:
                st.download_button("Download Summary", f, file_name=os.path.basename(summary_path))

if __name__ == "__main__":
    main()

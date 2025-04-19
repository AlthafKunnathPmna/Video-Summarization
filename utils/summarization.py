import torch
from transformers import pipeline
import google.generativeai as genai
from utils.pdf_utils import convert_to_pdf
from utils.video_processing import extract_frames_audio, filter_frames
from utils.text_processing import transcript_audio, extract_text_from_video, combine_text

def summarize(input_file, max_len, min_len, sum_model, output_path, device=0):
    summarizer = pipeline("summarization", model=sum_model, torch_dtype=torch.float16, device=device)
    with open(input_file, "r") as f:
        text = f.read()
    chunks = [text[i:i+1024] for i in range(0, len(text), 1024)]
    summaries = [summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text'] for chunk in chunks]
    with open(output_path, "w") as f:
        f.write("\n".join(summaries))

def google_gemini(input_file, output_path='final_summary.md'):
    with open(input_file, 'r') as f:
        info = f.read()
    genai.configure(api_key="YOUR_API_KEY")
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(f"Give me a structured summary:\n{info}")
    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(response.text)

def process_video(video_path, summary_type, progress_bar):
    frames_dir, filtered_dir = "frames", "filtered_frames"
    audio_path, transcript = "audio.wav", "transcription.txt"
    frame_text, combined = "text_from_video_frames.txt", "combined.txt"
    summary_txt, summary_pdf = "summary_long.txt", "summary.pdf"

    progress_bar.progress(10, text="Extracting frames and audio...")
    extract_frames_audio(video_path, frames_dir, audio_name=audio_path)

    progress_bar.progress(30, text="Transcribing audio...")
    transcript_audio(audio_path, transcript)

    progress_bar.progress(50, text="Filtering frames...")
    filter_frames(frames_dir, filtered_dir)

    progress_bar.progress(70, text="Extracting text from frames...")
    extract_text_from_video(filtered_dir, frame_text)

    progress_bar.progress(80, text="Combining texts...")
    combine_text(transcript, frame_text, combined)

    progress_bar.progress(90, text="Summarizing...")
    if summary_type == "Structured Summary":
        summarize(combined, max_len=150, min_len=40, sum_model="facebook/bart-large-cnn", output_path=summary_txt)
        google_gemini(summary_txt, output_path='final_summary.md')
        convert_to_pdf('final_summary.md', summary_pdf, parse=True)
    else:
        summarize(transcript, max_len=70, min_len=20, sum_model="facebook/bart-large-cnn", output_path='summary_short.md')
        convert_to_pdf('summary_short.md', summary_pdf, parse=False)

    progress_bar.progress(100, text="Done!")
    return summary_pdf

import subprocess
import os
from PIL import Image
import imagehash

def extract_frames_audio(video_path, frames_dir, frame_interval=0.5, audio_name='audio.wav'):
    os.makedirs(frames_dir, exist_ok=True)
    subprocess.run(["ffmpeg", "-i", video_path, "-vf", f"fps={frame_interval}", f"{frames_dir}/frame_%04d.jpg"])
    subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_name, '-y'])

def filter_frames(input_folder, output_folder, threshold=5):
    os.makedirs(output_folder, exist_ok=True)
    hashes = []
    for filename in sorted(os.listdir(input_folder)):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            img_hash = imagehash.phash(img)
            if all(img_hash - h > threshold for h in hashes):
                hashes.append(img_hash)
                img.save(os.path.join(output_folder, filename))

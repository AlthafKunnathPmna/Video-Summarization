import whisper
import easyocr
import os

def transcript_audio(audio_path, output_path="transcription.txt"):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    with open(output_path, "w") as f:
        f.write(result["text"])

def extract_text_from_video(frame_folder, output_file='text_from_video_frames.txt'):
    reader = easyocr.Reader(['en'])
    combined_text = ""
    for img_name in sorted(os.listdir(frame_folder)):
        result = reader.readtext(os.path.join(frame_folder, img_name))
        text = '\n'.join([entry[1] for entry in result])
        combined_text += f"Text from {img_name}:\n{text}\n{'-'*40}\n"
    with open(output_file, "w") as f:
        f.write(combined_text)

def combine_text(input1, input2, output):
    with open(output, 'w') as outfile:
        for file in [input1, input2]:
            with open(file, 'r') as infile:
                outfile.write(infile.read())
            outfile.write("\n")

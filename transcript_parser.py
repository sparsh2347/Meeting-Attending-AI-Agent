import re
import os

# Tell Python exactly where to find ffmpeg.exe
#Download the ffmpeg file and use that path here 
#also upload the path to the system environment variables before using the script
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

# function to clean the timestamps from the transcript file to give the description of the metting in a better format
def clean_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    # Detect and remove timestamps (e.g., 00:01:02,000 --> 00:01:05,000)
    clean = re.sub(r'\d{2}:\d{2}:\d{2}[,.:]\d{3} --> \d{2}:\d{2}:\d{2}[,.:]\d{3}', '', raw)
    # Remove subtitle sequence numbers if present (like in .srt)
    clean = re.sub(r'^\d+\n', '', clean, flags=re.MULTILINE)
    # Remove extra whitespace
    clean = re.sub(r'\n+', '\n', clean)
    
    return clean.strip()

import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("base")  # or "small", "medium", "large" based on accuracy/speed tradeoff
    result = model.transcribe(file_path)
    return result['text']



import openai
import re
import os
import time

# Tell Python exactly where to find ffmpeg.exe
#Download the ffmpeg file and use that path here 
#also upload the path to the system environment variables before using the script
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

import whisper
import dateparser
from datetime import datetime
from calendar_integartion import add_event_to_calendar
from summarizer import summarize_meeting
from transcript_parser import transcribe_audio, clean_transcript
from dotenv import load_dotenv

# === SETUP ===
# Extend PATH to include FFmpeg for audio handling (needed by Whisper)
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

# Load environment variables from .env file (for secure API keys)
load_dotenv()

# === AZURE OPENAI CONFIGURATION ===
openai.api_type = "azure"
openai.api_base = "https://mindcraft-kapidhwaj-openai-api-key.openai.azure.com/"
openai.api_version = "2024-12-01-preview"


#Here use your openai key (generally load it into .env file for better safety)
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
deployment_name = "mindcraft-gpt4o"

# === UTILITY: Convert Natural Language Date → ISO Date ===
def convert_to_date(due_str):
    date = dateparser.parse(due_str, settings={'PREFER_DATES_FROM': 'future'})
    return date.strftime('%Y-%m-%d') if date else None

#Here takes the summary text and extract the action items in a proper format to give to calendar_integration script

# === GPT-4o: Extract Action Items from Meeting Summary ===
def extract_action_items(summary_text):
    retries = 5
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an assistant that extracts action items from a meeting summary.\n"
                            "Return each item in this **structured format**:\n\n"
                            "- task: <task description>\n"
                            "  person: <name>\n"
                            "  due: <due date in ISO format: YYYY-MM-DD>\n\n"
                            "⚠️ Important: ALWAYS convert due dates like 'next Friday' or 'tomorrow' "
                            "into actual ISO dates assuming today's date is "
                            f"{datetime.today().strftime('%Y-%m-%d')}."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Meeting Summary:\n{summary_text}"
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response["choices"][0]["message"]["content"]
        except openai.error.RateLimitError as e:
            wait = 2 ** attempt
            print(f"Rate limited. Retrying in {wait} seconds...")
            time.sleep(wait)

#function to schedule all the action items extracted with proper description on the specified date
# === Google Calendar Scheduler ===
def schedule_action_items(action_text):
    # Match structured task info from GPT output
    pattern = r"- task: (.*?)\n\s+person: (.*?)\n\s+due: (.*?)(?:\n|$)"
    matches = re.findall(pattern, action_text)
    print(matches)

    # Loop through each action item
    for task, person, due in matches:
        date_str = convert_to_date(due)
        if date_str:
            print(f"📆 Scheduling: {task} for {person} on {date_str}")
            add_event_to_calendar(
                summary=f"{person}: {task}",
                date_str=date_str,
                description="From meeting notes"
            )
        else:
            print(f"⚠️ Could not parse date: {due}")

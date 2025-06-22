import streamlit as st
import os
from datetime import datetime
from transcript_parser import transcribe_audio, clean_transcript
from summarizer import summarize_meeting
from calendar_integartion import add_event_to_calendar
from ai_agent import extract_action_items, schedule_action_items

# Create a directory to store uploaded audio files if it doesn't exist
if not os.path.exists("audio"):
    os.makedirs("audio")

# Configure the Streamlit page settings
st.set_page_config(page_title="Meeting AI Agent", layout="centered")

# Display the main title of the application
st.title("🤖 Meeting Insights & Follow-Up Agent")

# Allow the user to choose their preferred input method
mode = st.radio("Choose input type:", ["Upload Audio File", "Paste Transcript", "Upload Transcript File"])

transcript_text = "" # Initialize variable to hold the transcript content

# ---
# Handle Transcript Input Methods
# ---
if mode == "Upload Transcript File":
    # File uploader for text or subtitle files
    uploaded_file = st.file_uploader("Upload transcript file (.txt or .srt)", type=["txt", "srt", "md"])
    if uploaded_file is not None:
        transcript_text = uploaded_file.read().decode("utf-8") # Read and decode the file content
        st.success("Transcript loaded successfully.")
        transcript_text = clean_transcript(transcript_text) # Clean the loaded transcript
        st.text_area("Transcript Preview:", transcript_text, height=200) # Show preview

elif mode == "Upload Audio File":
    # File uploader for audio files
    audio_file = st.file_uploader("Upload meeting audio (.mp3 or .wav)", type=["mp3", "wav"])
    if audio_file is not None:
        save_path = os.path.join("audio", audio_file.name) # Define path to save the audio
        with open(save_path, "wb") as f:
            f.write(audio_file.getbuffer()) # Save the uploaded audio
        st.success("Audio uploaded successfully.")

        with st.spinner("Transcribing audio..."):
            transcript_text = transcribe_audio(save_path) # Transcribe the audio file
            st.text_area("Transcript:", transcript_text, height=200) # Display transcribed text

else: # This covers the "Paste Transcript" option
    transcript_text = st.text_area("Paste your meeting transcript here", height=200)

# ---
# Process Transcript for Summary and Action Items
# ---
if transcript_text:
    # Button to start the analysis process
    if st.button("Generate Summary and Action Items"):
        summary = summarize_meeting(transcript_text) # Generate meeting summary
        st.session_state['summary'] = summary # Store summary in session state
        items = extract_action_items(summary) # Extract action items from the summary
        st.session_state['items'] = items # Store action items in session state

    # Display the generated summary if available
    if 'summary' in st.session_state:
        st.subheader("📝 Summary")
        st.markdown(st.session_state['summary'])

    # Display the extracted action items if available
    if 'items' in st.session_state:
        st.subheader("📌 Action Items")
        st.code(st.session_state['items']) # Display action items

        # Button to schedule action items to Google Calendar
        if st.button("📆 Schedule All to Google Calendar"):
            schedule_action_items(st.session_state['items']) # Call function to schedule tasks
            st.success("All tasks scheduled!")
from __future__ import print_function
import datetime
import os
import pickle

# Google API libraries
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# ✅ Define the required permission scope for Google Calendar API
# This gives the app permission to view and manage calendar events.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """
    Authenticates the user and returns a Google Calendar API service object.
    Handles both first-time authentication and token reuse.
    """
    creds = None

    # ✅ Load existing credentials from token.pickle if available
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # ✅ If no valid credentials are found, initiate login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # ✅ Refresh expired token
            creds.refresh(Request())
        else:
            #Keep the json credentials file within the same file structure and use that path here
            CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
            # ✅ Load client secret path from environment or fallback
            CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

            # ✅ Starts the OAuth2 flow using your downloaded credentials.json
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)

            # ✅ This opens a local server and browser login window
            creds = flow.run_local_server(port=0)

        # ✅ Save the authenticated token to reuse in future runs
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # ✅ Create and return the authenticated Google Calendar API service object
    service = build('calendar', 'v3', credentials=creds)
    return service

#function to add an event to the calendar taking the description and date as input on which the event would be created
def add_event_to_calendar(summary, date_str, description="Meeting Action Item"):
    """
    Schedules an event on the user's primary Google Calendar.

    Args:
        summary (str): Title of the event (e.g. "Alice: Finalize report")
        date_str (str): ISO date (YYYY-MM-DD) of the task deadline
        description (str): Optional detailed description of the task
    """
    service = get_calendar_service()

    # ✅ Create an event dictionary to send to Google Calendar
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': date_str + 'T09:00:00',  # Start time
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': date_str + 'T10:00:00',  # End time (1 hour duration)
            'timeZone': 'Asia/Kolkata',
        },
    }

    #This creates an event with the description above on the specified date 
    # ✅ Insert the event into the user's calendar
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Event created: {event.get('htmlLink')}")

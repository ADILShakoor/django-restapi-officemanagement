
import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

BASE_DIR = settings.BASE_DIR
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')

def get_google_flow():
    return Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/oauth2callback/'
    )

def get_calendar_service(credentials):
    return build('calendar', 'v3', credentials=credentials)

def create_google_calendar_event(credentials, event_data):
    service = get_calendar_service(credentials)

    event = {
        'summary': event_data['title'],
        'location': event_data.get('location', ''),
        'description': event_data.get('description', ''),
        'start': {
            'dateTime': event_data['start_time'].isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': event_data['end_time'].isoformat(),
            'timeZone': 'UTC',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event

def update_google_calendar_event(credentials, event_id, event_data):
    service = get_calendar_service(credentials)

    updated_event = {
        'summary': event_data['title'],
        'location': event_data.get('location', ''),
        'description': event_data.get('description', ''),
        'start': {
            'dateTime': event_data['start_time'].isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': event_data['end_time'].isoformat(),
            'timeZone': 'UTC',
        },
    }

    event = service.events().update(
        calendarId='primary',
        eventId=event_id,
        body=updated_event
    ).execute()

    return event


def delete_google_calendar_event(credentials, event_id):
    service = get_calendar_service(credentials)
    service.events().delete(calendarId='primary', eventId=event_id).execute()


# This script demonstrates how to create an event in Google Calendar using the Google Calendar API. 
# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build
# import datetime

# # Path to your credentials.json file
# CREDENTIALS_FILE = "credentials.json"

# # Scopes for Google Calendar API
# SCOPES = ['https://www.googleapis.com/auth/calendar']

# def get_calendar_service():
#     """Authenticate and return the Google Calendar service."""
#     credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
#     service = build('calendar', 'v3', credentials=credentials)
#     return service

# def create_event(summary, location, description, start_time, end_time, timezone='UTC'):
#     """
#     Create an event in the Google Calendar.
    
#     Args:
#         summary (str): Title of the event.
#         location (str): Location of the event.
#         description (str): Description of the event.
#         start_time (str): Start time in ISO format (e.g., '2023-10-01T10:00:00').
#         end_time (str): End time in ISO format (e.g., '2023-10-01T11:00:00').
#         timezone (str): Timezone for the event (default is 'UTC').
#     """
#     service = get_calendar_service()
#     event = {
#         'summary': summary,
#         'location': location,
#         'description': description,
#         'start': {
#             'dateTime': start_time,
#             'timeZone': timezone,
#         },
#         'end': {
#             'dateTime': end_time,
#             'timeZone': timezone,
#         },
#     }
#     created_event = service.events().insert(calendarId='primary', body=event).execute()
#     print(f"Event created: {created_event.get('htmlLink')}")

# if __name__ == "__main__":
#     # Example usage
#     create_event(
#         summary="Team Meeting",
#         location="Office Conference Room",
#         description="Discuss project updates and next steps.",
#         start_time="2023-10-01T10:00:00",
#         end_time="2023-10-01T11:00:00",
#         timezone="UTC"
#     )
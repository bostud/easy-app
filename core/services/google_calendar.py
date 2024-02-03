import datetime
import os
from typing import List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from core.services.api_client import ApiClientABC


class GoogleCalendarAdapter(ApiClientABC):
    def __init__(self, credentials_file: str, token_file: str) -> None:
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        self.credentials_file = credentials_file
        self.token_file = token_file

    def authenticate(self):
        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes)
                creds = flow.run_local_server(port=0)

            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        return creds

    def create_event(self, event_details: dict) -> dict:
        service = build(
            'calendar',
            'v3',
            credentials=self.authenticate(),
        )

        event = {
            'summary': event_details['title'],
            'description': event_details['description'] or "",
            'start': {
                'dateTime': event_details['start_datetime'],
                'timeZone': 'UTC',
            },
        }

        event = service.events().insert(
            calendarId='primary',
            body=event,
        ).execute()
        return event

    def get_events(self, for_date: datetime.date) -> List[dict]:
        service = build('calendar', 'v3', credentials=self.authenticate())

        start_time = f'{for_date}T00:00:00Z'
        end_time = f'{for_date}T23:59:59Z'

        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime',
        ).execute()

        events = events_result.get('items', [])
        return events

    def delete_event(self, event_id: str) -> dict:
        service = build('calendar', 'v3', credentials=self.authenticate())

        try:
            service.events().delete(
                calendarId='primary',
                eventId=event_id,
            ).execute()
            return {"status": "Deleted"}
        except Exception as e:
            print(f'Error deleting event: {e}')
            return {"status": "Error", "message": str(e)}

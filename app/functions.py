from google.oauth2 import service_account
from googleapiclient.discovery import build
from dateutil import parser
from datetime import timedelta

def create_calendar_event(name, datetime_str):
  endtime_obj = parser.parse(datetime_str)
  end_datetime_obj = endtime_obj + timedelta(hours=1)
  endtime = end_datetime_obj.isoformat()

  SERVICE_ACCOUNT_FILE = 'credentials_info.json'
  SCOPES = ['https://www.googleapis.com/auth/calendar']
  credentials = service_account.Credentials.from_service_account_file(
          SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  service = build('calendar', 'v3', credentials=credentials)
  event = {
      'summary': name,
      'start': {
          'dateTime': datetime_str,
          'timeZone': 'America/Denver',
      },
      'end': {
          'dateTime': endtime,
          'timeZone': 'America/Denver',
      },
  }

  calendar_id = 'temuge.max12@gmail.com'
  event = service.events().insert(calendarId=calendar_id, body=event).execute()
  return event
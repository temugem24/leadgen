import schedule
import time
from twilio.rest import Client
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from .config import settings

load_dotenv()

client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
scopes_list = settings.scopes.split(',')

def get_unsent_rows():

  credentials = service_account.Credentials.from_service_account_file(
      settings.service_account_file, scopes=scopes_list)
  service = build('sheets', 'v4', credentials=credentials)
  result = service.spreadsheets().values().get(
    spreadsheetId=settings.spreadsheet_id, 
    range=settings.range_name
    ).execute()
  values = result.get('values', [])
  unsent_rows = []

  for index, row in enumerate(values, start=1):
      if len(row) > 3 and row[3].strip() == "Not Sent":  
          phone_number = row[2].strip() if len(row) > 3 else None  
          unsent_rows.append((index, phone_number)) 

  return unsent_rows

def send_init_messages():
  unsent_leads = get_unsent_rows()
  message_text = "HEyOOOOO"
  for index, phone_number in unsent_leads:
      if phone_number: 
          try:
              message_response = client.messages.create(
                  body=message_text,
                  from_='whatsapp:+14155238886',  
                  to=f'whatsapp:{phone_number}'
              )
            
              status_cell = f'Sheet1!D{index}' 
              update_status_in_sheet(status_cell)
              print(f"Message sent to {phone_number}: {message_response.sid}")
          except Exception as e:
              print(f"Failed to send message to {phone_number}: {str(e)}")

def update_status_in_sheet(range_to_update):
  credentials = service_account.Credentials.from_service_account_file(
      settings.service_account_file, scopes=scopes_list)
  service = build('sheets', 'v4', credentials=credentials)
  values = [["Sent"]]  
  body = {'values': values}
  try:
      result = service.spreadsheets().values().update(
          spreadsheetId=settings.spreadsheet_id, range=range_to_update,
          valueInputOption="USER_ENTERED", body=body).execute()
      print(f"Successfully updated {result.get('updatedCells')} cells to 'Sent' at {range_to_update}")
  except Exception as e:
      print(f"Failed to update {range_to_update}: {e}")

def run_scheduler():
    schedule.every(10).seconds.do(send_init_messages)

    while True:
        schedule.run_pending()
        time.sleep(1)



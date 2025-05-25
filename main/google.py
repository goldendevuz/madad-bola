import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from icecream import ic

# Get the absolute path to the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate from bot/utils/ to core/data/
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, '..', 'core', 'data', 'service-account.json')
SERVICE_ACCOUNT_FILE = os.path.abspath(SERVICE_ACCOUNT_FILE)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_google_services():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    sheets_service = build('sheets', 'v4', credentials=creds)
    return creds, sheets_service

def get_user_rows(sheet_id, sheet_name="responses"):
    range_name = f"{sheet_name}!A2:Y"  # First 4 columns (Timestamp, Name, Phone, Telegram)
    ic(sheet_id, range_name)
    _, sheets_service = get_google_services()

    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_name
    ).execute()
    # ic(result)

    rows = result.get("values", [])
    # ic(rows)
    user_rows = []
    for row in rows:
        if row[22] == rows[-1][22]:
            user_rows.append(row)
    # ic(user_rows)
    return user_rows

def get_result_rows(sheet_id, sheet_name="result"):
    range_name = f"{sheet_name}!A1:B19"  # First 4 columns (Timestamp, Name, Phone, Telegram)
    ic(sheet_id, range_name)
    _, sheets_service = get_google_services()

    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_name
    ).execute()
    # ic(result)

    rows = result.get("values", [])
    ic(rows)
    return rows

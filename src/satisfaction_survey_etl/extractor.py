import os.path
import pickle
from typing import List

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.common import CONFIG


def extract_survey_data() -> List[dict]:
    SPREADSHEET_ID = CONFIG['google_sheets_spreadsheet_id']
    RANGE_NAME = CONFIG['google_sheets_range_name']
    sheet = _sheet_connection()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values


def _sheet_connection():
    PICKLE_FILEPATH = CONFIG['google_sheets_pickle_filepath']
    CREDENTIALS_FILEPATH = CONFIG['google_sheets_credentials_filepath']
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = None
    if os.path.exists(PICKLE_FILEPATH):
        with open(PICKLE_FILEPATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILEPATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(PICKLE_FILEPATH, 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds).spreadsheets()

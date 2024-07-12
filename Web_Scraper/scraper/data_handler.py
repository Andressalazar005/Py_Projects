import pandas as pd
import requests
import json
import re
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def load_client_config(file_path="credentials/credentials.json"):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_to_csv(data, filename="scraped_data.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def extract_spreadsheet_id(url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Google Sheets URL format")

def get_authenticated_session(client_config, token_file="credentials/token.json"):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, ["https://www.googleapis.com/auth/spreadsheets"])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(client_config, ["https://www.googleapis.com/auth/spreadsheets"])
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {creds.token}'})
    return session

def upload_to_google_sheets(data, spreadsheet_url, range_name="Sheet1!A1", token_file="credentials/token.json"):
    client_config = load_client_config()

    try:
        spreadsheet_id = extract_spreadsheet_id(spreadsheet_url)
    except ValueError as e:
        print(f"Error: {e}")
        return False

    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}:append?valueInputOption=RAW"
    headers = {"Content-Type": "application/json"}
    payload = {
        "range": range_name,
        "majorDimension": "ROWS",
        "values": data  # Ensure the correct data structure
    }

    try:
        session = get_authenticated_session(client_config, token_file)
        response = session.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as error:
        print(f"Error uploading to Google Sheets: {error}")
        return False


import pandas as pd
import requests
import json
import re
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def prepare_data(data):
    aggregated_data = {}
    seen_composite_keys = set()

    # Aggregating data by composite key (name and URL)
    for item in data:
        name = item.get('name', '')
        url = item.get('URL')
        composite_key = (name, url)
        
        if url and all(value for key, value in item.items() if key != 'URL'):
            if composite_key not in seen_composite_keys:
                seen_composite_keys.add(composite_key)
                aggregated_data[composite_key] = item
            else:
                aggregated_data[composite_key].update(item)

    headers = sorted(set(key for item in aggregated_data.values() for key in item.keys()))

    # Ensure 'name' is the first header and 'URL' is the last header
    if 'name' in headers:
        headers.remove('name')
    if 'URL' in headers:
        headers.remove('URL')
    headers = ['name'] + headers + ['URL']

    # Creating a list of rows from the aggregated data
    prepared_data = [
        [item.get(header, "") for header in headers]
        for item in aggregated_data.values()
    ]

    # Log the aggregated data for debugging
    logging.info(f"Aggregated Data: {json.dumps(prepared_data, indent=2)}")

    return headers, prepared_data


def upload_to_google_sheets(data, spreadsheet_url, range_name="Sheet1!A1", token_file="credentials/token.json"):
    client_config = load_client_config()

    try:
        spreadsheet_id = extract_spreadsheet_id(spreadsheet_url)
    except ValueError as e:
        logging.error(f"Error: {e}")
        return False

    headers, values = prepare_data(data)

    # Include headers as the first row
    values = [headers] + values

    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}:append?valueInputOption=RAW"
    headers = {"Content-Type": "application/json"}
    payload = {
        "range": range_name,
        "majorDimension": "ROWS",
        "values": values
    }

    # Debugging: Print the payload to verify the structure
    logging.info(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        session = get_authenticated_session(client_config, token_file)
        response = session.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logging.info("Data successfully uploaded to Google Sheets.")
        return True
    except requests.exceptions.HTTPError as error:
        logging.error(f"Error uploading to Google Sheets: {error}")
        logging.error(f"Response: {error.response.content}")
        return False

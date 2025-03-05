import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

def load_data_from_sheets(spreadsheet_id, range_name, credentials_path="credentials.json"):
    """Loads data from a Google Sheet into a Pandas DataFrame.

    Args:
        spreadsheet_id (str): The ID of the Google Sheet.
        range_name (str): The range of cells to retrieve (e.g., 'Sheet1!A1:J100').
        credentials_path (str): Path to the credentials.json file.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the sheet, or None if an error occurred.
    """
    try:
        # Load credentials
        creds = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

        # Build the Google Sheets service
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return None

        # Convert to DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])  # First row as header

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

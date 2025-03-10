import gspread
import pandas as pd
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate_oauth(credentials_file):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds


def authenticate_oauth(credentials_file, token_file="token.json"):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = None
    if os.path.exists(token_file):  # Controlla se esiste già un token salvato
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:  # Se non è valido, richiede una nuova autenticazione
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)

        # Salva il nuovo token per il futuro
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds

def download_google_sheet(spreadsheet_id, sheet_name, output_file, credentials_file, token_file="token.json"):
    print("Starting")

    #creds = authenticate_oauth(credentials_file)
    creds = authenticate_oauth(credentials_file, token_file)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
    data = sheet.get_all_values()
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, header=False)
    print(f"File salvato come {output_file}")

# Esempio di utilizzo
if __name__ == "__main__":

    spreadsheet_id = "1e8ZFzwKBgURyGTJnbJ9USw6vlF8gAv6NumPj7r74T7k"
    sheet_name = "Foglio1"
    output_file = "output.csv"
    credentials_file = "credentials.json"
    
    download_google_sheet(spreadsheet_id, sheet_name, output_file, credentials_file)

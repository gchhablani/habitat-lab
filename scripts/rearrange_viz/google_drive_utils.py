import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload


def load_credentials(token_file_path, scopes):
    creds = None
    if os.path.exists('tokens.json'):
        creds = Credentials.from_authorized_user_file('tokens.json', scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                token_file_path, scopes
            )
            creds = flow.run_local_server(port=0)
        with open('tokens.json', "w") as token:
            token.write(creds.to_json())
    return creds


def create_drive_folder(service, folder_name):
    # Check if the folder already exists
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    response = service.files().list(q=query, fields="files(id)").execute()
    folders = response.get("files", [])

    # If the folder exists, return its ID
    if folders:
        return folders[0]["id"]
    else:
        # If the folder doesn't exist, create a new one
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')


def upload_image_to_drive(service, folder_id, image_path):
    file_name = os.path.basename(image_path)
    
    # Check if file with the same name already exists in the folder
    existing_file = service.files().list(q=f"name='{file_name}' and '{folder_id}' in parents", fields='files(id)').execute()
    
    if existing_file.get('files', []):
        existing_file_id = existing_file['files'][0]['id']
        # Delete existing file
        service.files().delete(fileId=existing_file_id).execute()
    
    file_metadata = {
        'name': file_name,
        'parents': [folder_id],
        'mimeType': 'image/png',
    }
    media = MediaFileUpload(image_path, mimetype='image/png')
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    image_url = file.get('webViewLink')
    return file.get('id'), image_url

# def get_google_sheet(creds_path, sheet_name, scope):
#     creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
#     client = gspread.authorize(creds)
#     sheet = client.open(sheet_name).sheet1
#     return sheet

def get_google_sheet(service, sheet_name, sheet_id=None):
    if sheet_id:
        # Just verifying that the sheet exists
        existing_spreadsheet = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        spreadsheet_id = existing_spreadsheet['spreadsheetId']
    else:
        # Create a new spreadsheet
        spreadsheet = {
            "properties": {
                "title": sheet_name
            }
        }
        created_spreadsheet = (
            service.spreadsheets()
            .create(body=spreadsheet, fields="spreadsheetId")
            .execute()
        )
        spreadsheet_id = created_spreadsheet['spreadsheetId']
    return spreadsheet_id

def add_image_to_sheet(service, sheet_id, episode_id, image_id):
    template = '=IMAGE("https://drive.google.com/uc?export=download&id=' + image_id + '", 1)'
    range_name = f'Sheet1!A{episode_id+2}:B{episode_id+2}'
    # Construct the request body
    body = {
        'values': [
            [episode_id, template]
        ]
    }
    
    # Append values to the spreadsheet
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    return result
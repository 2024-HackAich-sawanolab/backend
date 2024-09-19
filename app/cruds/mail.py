from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import email

def get_all_emails(access_token):
    creds = Credentials(token=access_token)
    service = build('gmail', 'v1', credentials=creds)
    messages = []
    try:
        response = service.users().messages().list(userId='me').execute()
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', pageToken=page_token).execute()
            if 'messages' in response:
                messages.extend(response['messages'])
        print(f"取得したメッセージ数: {len(messages)}")
        for msg in messages:
            msg_id = msg['id']
            message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            
            # メッセージのペイロードを解析
            payload = message.get('payload', {})
            headers = payload.get('headers', [])
            parts = payload.get('parts', [])
            
            # ヘッダー情報の取得
            subject = ''
            from_ = ''
            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                elif header['name'] == 'From':
                    from_ = header['value']
            
            # 本文の取得
            body = get_body_from_parts(parts)
            
            print(f"From: {from_}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")
            print("-----")
    except Exception as error:
        print(f'エラーが発生しました: {error}')

def get_body_from_parts(parts):
    """
    メッセージのペイロードから本文を抽出する
    """
    if not parts:
        return ""
    
    for part in parts:
        mime_type = part.get('mimeType')
        filename = part.get('filename')
        body = part.get('body', {})
        data = body.get('data')
        parts_nested = part.get('parts')
        
        if mime_type == 'text/plain' and data:
            return decode_base64(data)
        elif mime_type == 'text/html' and data:
            return decode_base64(data)
        elif parts_nested:
            return get_body_from_parts(parts_nested)
    
    return ""

def decode_base64(data):
    """
    Base64エンコードされたデータをデコードする
    """
    decoded_bytes = base64.urlsafe_b64decode(data.encode('ASCII'))
    try:
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        decoded_str = decoded_bytes.decode('latin1')
    return decoded_str
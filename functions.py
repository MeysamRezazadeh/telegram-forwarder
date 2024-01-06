import requests
from config import Config

async def send_file_to_eitaa(file, text=None):
    files = {'file': file}
    payload = {'chat_id': Config.EITAA_CHAT_ID}
    if text:
        payload['caption'] = text

    response = requests.post(Config.EITAA_API_FILE, data=payload, files=files)
    return response

async def send_file_to_bale(file, text=None, file_type=None):
    if file_type == "photo":
        files = {'photo': file}
        bale_api_file = Config.BALE_API_PHOTO
    elif file_type == "video":
        files = {'video': file}
        bale_api_file = Config.BALE_API_VIDEO
    else:
        files = {'document': file}
        bale_api_file = Config.BALE_API_DOCUMENT

    payload = {'chat_id': Config.BALE_CHAT_ID}
    if text:
        payload['caption'] = text

    response = requests.post(bale_api_file, data=payload, files=files)
    return response

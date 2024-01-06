import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SEND_EITAA = os.environ.get("SEND_EITAA") == 'true'
    EITAA_API_MESSAGE = f'https://eitaayar.ir/api/{os.environ.get("EITAA_BOT_TOKEN")}/sendMessage'
    EITAA_API_FILE = f'https://eitaayar.ir/api/{os.environ.get("EITAA_BOT_TOKEN")}/sendFile'
    
    SEND_BALE = os.environ.get("SEND_BALE") == 'true'
    BALE_API_MESSAGE = f'https://tapi.bale.ai/bot{os.environ.get("BALE_BOT_TOKEN")}/sendMessage'
    BALE_API_PHOTO = f'https://tapi.bale.ai/bot{os.environ.get("BALE_BOT_TOKEN")}/SendPhoto'
    BALE_API_VIDEO = f'https://tapi.bale.ai/bot{os.environ.get("BALE_BOT_TOKEN")}/SendVideo'
    BALE_API_DOCUMENT = f'https://tapi.bale.ai/bot{os.environ.get("BALE_BOT_TOKEN")}/SendDocument'
    
    EITAA_CHAT_ID = os.environ.get("EITAA_CHAT_ID")
    BALE_CHAT_ID = os.environ.get("BALE_CHAT_ID")
    
    TELEGRAM_GROUP_ID = os.environ.get("TELEGRAM_GROUP_ID")
    TELEGRAM_DEBUG_ID = os.environ.get("TELEGRAM_DEBUG_ID")
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")

    ALLOWED_USERNAMES = os.environ.get("ALLOWED_USERNAMES");

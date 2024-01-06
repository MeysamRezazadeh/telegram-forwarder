import os
import requests
from config import Config
from telethon import TelegramClient, events
from functions import send_file_to_eitaa, send_file_to_bale


client = TelegramClient('session_name', Config.API_ID, Config.API_HASH)
client.start()

async def handle_media(event, media_type):
    message_text = f"""
➖➖➖➖➖➖➖➖➖➖
⏳ دانلود فایل: درحال دانلود {'عکس' if media_type == 'photo' else 'فیلم'}...
🔴 ارسال به ایتا: 
🔴 ارسال به بله: 
➖➖➖➖➖➖➖➖➖➖
"""
    sent_message = await event.reply(message_text)
    media_file = await event.download_media()
    caption = event.raw_text if hasattr(event, 'message') else None
    with open(media_file, 'rb') as file:
        response = file.read()

    message_text = f"""
➖➖➖➖➖➖➖➖➖➖
✅ دانلود فایل: دانلود با موفقیت انجام شد
🔴 ارسال به ایتا: 
🔴 ارسال به بله: 
➖➖➖➖➖➖➖➖➖➖
"""
    sent_message = await client.edit_message(event.chat_id, sent_message, message_text)

    # Send to eitaa
    if Config.SEND_EITAA:
        message_text = message_text.replace(f"🔴 ارسال به ایتا: ", f"⏳ ارسال به ایتا: در حال ارسال {media_type}...")
        try:
            sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
            eitaa_response = await send_file_to_eitaa(response, caption)
            if eitaa_response.json()['ok'] == True:
                message_text = message_text.replace(f"⏳ ارسال به ایتا: در حال ارسال {media_type}...", f"✅ ارسال به ایتا: با موفقیت ارسال شد")
                sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
            else:
                message_text = message_text.replace(f"⏳ ارسال به ایتا: در حال ارسال {media_type}...", f"❌ ارسال به ایتا: مشکل در ارسال")
                sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
        except Exception as e:
            message_text = message_text.replace(f"⏳ ارسال به ایتا: در حال ارسال {media_type}...", f"❌ ارسال به ایتا: مشکل در ارسال")
            sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
            await client.send_message(int(Config.TELEGRAM_DEBUG_ID), f"Failed to send {media_type} to Eitaa: {e}")
    else:
        message_text = message_text.replace(f"🔴 ارسال به ایتا: ", f"⚠️ ارسال به ایتا: غیرفعال")
        sent_message = await client.edit_message(event.chat_id, sent_message, message_text)

    # Send to bale
    if Config.SEND_BALE:
        message_text = message_text.replace(f"🔴 ارسال به بله: ", f"⏳ ارسال به بله: در حال ارسال {media_type}...")
        try:
            sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
            bale_response = await send_file_to_bale(response, caption, media_type)
            if bale_response.json()['ok'] == True:
                message_text = message_text.replace(f"⏳ ارسال به بله: در حال ارسال {media_type}...", f"✅ ارسال به بله: با موفقیت ارسال شد")
                sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
            else:
                message_text = message_text.replace(f"⏳ ارسال به بله: در حال ارسال {media_type}...", f"❌ ارسال به بله: مشکل در ارسال")
                sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
        except Exception as e:
            message_text = message_text.replace(f"⏳ ارسال به بله: در حال ارسال {media_type}...", f"❌ ارسال به بله: مشکل در ارسال")
            sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
            await client.send_message(int(Config.TELEGRAM_DEBUG_ID), f"Failed to send {media_type} to Bale: {e}")
    else:
        message_text = message_text.replace(f"🔴 ارسال به بله: ", f"⚠️ ارسال به بله: غیرفعال.")
        sent_message = await client.edit_message(event.chat_id, sent_message, message_text)

    # Remove file
    if os.path.exists(media_file):
        os.remove(media_file)

@client.on(events.NewMessage)
async def channel_post_handler(event):
    channel_id = event.chat_id
    if channel_id == int(Config.TELEGRAM_GROUP_ID):
        sender_username = event.sender.username
        allowed_usernames = Config.ALLOWED_USERNAMES.split(',')

        if sender_username and sender_username in allowed_usernames:
            if Config.SEND_EITAA == False and Config.SEND_BALE == False:
                await event.reply("❗️ هیچ پیامرسان فعالی جهت ارسال وجود ندارد")
            else:
                # Check if it's a photo
                if event.photo and not hasattr(event.media, 'webpage'):
                    await handle_media(event, 'photo')
                # Check if it's a video
                elif event.media and not hasattr(event.media, 'webpage'):
                    await handle_media(event, 'video')
                # if it's a text message
                else:
                    message_text = """
➖➖➖➖➖➖➖➖➖➖
🔴 ارسال به ایتا: 
🔴 ارسال به بله: 
➖➖➖➖➖➖➖➖➖➖
"""
                    sent_message = await event.reply(message_text)

                    # send to eitaa
                    if Config.SEND_EITAA:
                        message_text = message_text.replace("🔴 ارسال به ایتا: ", "⏳ ارسال به ایتا: در حال ارسال...")
                        try:
                            sent_message = await client.edit_message(event.chat_id, sent_message, message_text)

                            eitaa_response = requests.post(Config.EITAA_API_MESSAGE, data={'chat_id': Config.EITAA_CHAT_ID, 'text': event.text})
                            if eitaa_response.json()['ok'] == True:
                                message_text = message_text.replace("⏳ ارسال به ایتا: در حال ارسال...", "✅ ارسال به ایتا: با موفقیت ارسال شد")
                                sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
                            else:
                                message_text = message_text.replace("⏳ ارسال به ایتا: در حال ارسال...", "❌ ارسال به ایتا: مشکل در ارسال")
                                sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
                        except Exception as e:
                            message_text = message_text.replace("⏳ ارسال به ایتا: در حال ارسال...", "❌ ارسال به ایتا: مشکل در ارسال")
                            sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
                            await client.send_message(int(Config.TELEGRAM_DEBUG_ID), f"Failed to send video to Eitaa: {e}")
                    else:
                        message_text = message_text.replace("🔴 ارسال به ایتا: ", "⚠️ ارسال به ایتا: غیرفعال")
                        sent_message = await client.edit_message(event.chat_id, sent_message, message_text)

                    # send to bale
                    if Config.SEND_BALE:
                        message_text = message_text.replace("🔴 ارسال به بله: ", "⏳ ارسال به بله: در حال ارسال...")
                        try:
                            sent_message = await client.edit_message(event.chat_id, sent_message, message_text)

                            bale_response = requests.post(Config.BALE_API_MESSAGE, data={'chat_id': Config.BALE_CHAT_ID, 'text': event.text})
                            if bale_response.json()['ok'] == True:
                                message_text = message_text.replace("⏳ ارسال به بله: در حال ارسال...", "✅ ارسال به بله: با موفقیت ارسال شد")
                                sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
                            else:
                                message_text = message_text.replace("⏳ ارسال به بله: در حال ارسال...", "❌ ارسال به بله: مشکل در ارسال")
                                sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
                        except Exception as e:
                            message_text = message_text.replace("⏳ ارسال به بله: در حال ارسال...", "❌ ارسال به بله: مشکل در ارسال")
                            sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
                            await client.send_message(int(Config.TELEGRAM_DEBUG_ID), f"Failed to send video to Bale: {e}")
                    else:
                        message_text = message_text.replace("🔴 ارسال به بله: ", "⚠️ ارسال به بله: غیرفعال.")
                        sent_message = await client.edit_message(event.chat_id, sent_message, message_text)
        
        else:
            await event.reply("❌ شما مجاز به استفاده از این ربات نیستید.")

client.run_until_disconnected()
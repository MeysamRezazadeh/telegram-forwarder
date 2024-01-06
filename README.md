# 🤖 Telegram Forwarder

Automate the forwarding of messages from a Telegram group to Iranian messaging platforms like Eitaa and Bale.

## 🚀 Overview

The "Telegram Forwarder" is a Python script designed to automate the forwarding of media files and text messages from Telegram to Iranian messaging platforms. It supports forwarding to Eitaa and Bale.


## 🛠️ Installation

To use this script, follow these installation steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/MeysamRezazadeh/telegram-forwarder.git
    cd telegram-forwarder
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    .\venv\Scripts\activate  # On Windows
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your environment variables:**

    Create a `.env` file with the following content:

    ```ini
    SEND_EITAA=true
    EITAA_BOT_TOKEN=your_eitaa_bot_token
    EITAA_CHAT_ID=your_eitaa_chat_id

    SEND_BALE=true
    BALE_BOT_TOKEN=your_bale_bot_token
    BALE_CHAT_ID=your_bale_chat_id

    TELEGRAM_GROUP_ID=your_telegram_group_id
    TELEGRAM_DEBUG_ID=your_telegram_debug_id
    API_ID=your_api_id
    API_HASH=your_api_hash
    ALLOWED_USERNAMES=allowed_username1,allowed_username2
    ```

    Replace the placeholders with your actual API tokens and chat IDs.

## 🛠️ Usage

Start the bot and send a file or message to your specified Telegram group.

```bash
python bot.py
```

## 📦 Dependencies

Python (>=3.x)
requests
python-dotenv
telethon (1.31.1)


## 🤝 Contributing

If you would like to contribute to the project, feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


<br /><br />


🌟 If you find this project helpful, please consider giving it a star.
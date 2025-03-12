
# Telegram ID Bot

This repository contains a simple Telegram bot built using Python and the `python-telegram-bot` library. The bot can help users retrieve various IDs and information from Telegram, such as user IDs and chat IDs.

## Features

- `/start`: Sends a welcome message with an introduction to the bot's commands.
- `/id`: Fetches and displays the user's Telegram ID.
- `/chatid`: Retrieves the current chat ID.
- `/info`: Provides detailed information about the user and the chat.

## Requirements

- Python 3.7 or higher
- Telegram Bot Token from [BotFather](https://core.telegram.org/bots#botfather)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/orcus-x/telegram-id-bot.git
   cd telegram-id-bot
   ```

2. Install the required dependencies:
   ```bash
   pip install python-telegram-bot
   ```

3. Replace `YOUR_BOT_TOKEN` in the script with your actual Telegram Bot Token.

## Usage

1. Run the bot:
   ```bash
   python id_bot.py
   ```

2. Start a chat with your bot on Telegram and use the commands:
   - `/start` to see the welcome message.
   - `/id` to get your user ID.
   - `/chatid` to get the current chat ID.
   - `/info` to get detailed information about yourself and the chat.

## Logging

This bot uses Python's built-in logging to display informational messages and errors in the console.

## Example Output

- `/id`
  ```
  Your Telegram ID is: 123456789
  ```

- `/chatid`
  ```
  Current chat ID is: -987654321
  ```

- `/info`
  ```
  👤 User Information
  • ID: `123456789`
  • First Name: John
  • Last Name: Doe
  • Username: @john_doe
  • Language: en
  
  💬 Chat Information
  • Chat ID: `-987654321`
  • Chat Type: group
  • Chat Title: My Group Chat
  ```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to improve this bot.

---

Happy coding! 🎉

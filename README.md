# Telegram Room Split Bot

A Telegram bot to help split room costs among group members during events or conventions.

## Features

- **Split Costs**: Calculate room cost splits based on the number of roommates and nights stayed.
- **Room Information**: Set and display room details like hotel name, dates, beds, and room type.
- **Roommates List**: Set and retrieve a list of roommates.
- **Acknowledgments**: Use inline buttons to acknowledge split messages, tracking who has seen the split.
- **Currency Support**: Set and display currency symbols (e.g., $, CAD, USD).
- **Reminders**: Send reminders to group members to settle expenses.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- A Telegram Bot Token (obtain from [BotFather](https://t.me/BotFather))
- Docker installed (for container deployment)

### Local Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/telegram-room-split-bot.git
   cd telegram-room-split-bot
   ```

2. **Create a Virtual Environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**
    Create a `.env` file and add your bot token:

    ```bash
    BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
    ```

5. **Run the Bot**

    ```bash
    python bot.py
    ```

### Docker Deployment

1. **Build the Docker Image**

    ```bash
    docker build -t telegram-room-split-bot .
    ```

2. **Run the Docker Container**

    ```bash
    docker run -d --name room-split-bot -e BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN telegram-room-split-bot
    ```

## Usage

- `/start`: Start the bot and get a welcome message.
- `/help`: List all available commands.
- `/split`: Calculate the split. Usage:
  - `/split <total_cost> <number_of_roommates> [names...] [nights_stayed...]`
  - Equal split without names example:
    `/split 1000 4`
  - Equal Split With Names
    `/split 1000 4 @Alice @Bob @Charlie @Dave`
  - Split Based on Nights Stayed With Names:
    `/split 1000 3 @Alice @Bob @Charlie 2 3 1`
  - Notes:
    - Order Matters: After <number_of_roommates>, provide names (if any), followed by nights stayed (if splitting by nights).
    - Names: Can be any text or @username
- `/currency`: Set or view the currency symbol.
- `/remind`: Send a reminder message.
- `/setroom`: Set room information.
  - The bot will prompt you to enter the room details in the format:
    `Hotel Name | Dates | Beds | Room Type`
- `/getroom`: Retrieve the current room information.
- `/setroommates`: Set the list of roommates.
  - The bot will prompt you to enter the roommates' names or usernames, separated by commas.

## Contribution Guidelines

1. Fork the Repository
2. Create a New Branch

    ```bash
    git checkout -b feature/YourFeature
    ```

3. Make Your Changes

4. Commit and Push

    ```bash
    git commit -m "Add YourFeature"
    git push origin feature/YourFeature
    ```

5. Create a Pull Request

## Future Enhancements

- Data Persistence: Integrate a database (e.g., SQLite, PostgreSQL) to store user settings and transaction history.
- User Permissions: Implement admin-only commands and restrict access as needed.
- Additional Features: Add support for handling multiple rooms, expenses tracking, and generating expense reports.

## Project Structure Overview

```bash
    telegram-room-split-bot/
    ├── bot.py
    ├── .env
    ├── .gitignore
    ├── Dockerfile
    ├── LICENSE
    ├── README.md
    ├── requirements.txt
    └── venv/
```

import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

#setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# read token from file
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

#create a bot instance
bot = Bot(token=TOKEN)

Updater = Updater(bot=bot)
dispatcher = Updater.dispatcher

#function to handling different commands
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am a bot!')

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

def main():
    # handlers for /start command
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # handlers for /help command
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)
    
    #start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

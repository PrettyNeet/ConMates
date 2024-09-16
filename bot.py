import os
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode
from collections import defaultdict


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Global variables
CURRENCY_SYMBOL = "$"

# In-memory storage (per chat)
acknowledgments = defaultdict(set)  # message_id: set of user_ids

# Conversation handler states
SET_ROOM_INFO = 1
SET_ROOMMATES = 2

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Room Split Bot! Type /help for available commands."
    )

# Command: /help
# this function is used to show the available commands.
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>Available Commands:</b>\n"
        "/start - Start the bot\n"
        "/help - List available commands\n"
        "/split &lt;total_cost&gt; &lt;number_of_roommates&gt; [names...] [nights_stayed...]\n"
        "/currency &lt;symbol&gt; - Set or view the currency symbol\n"
        "/remind - Send a reminder message\n"
        "/setroom - Set room information\n"
        "/getroom - Get room information\n"
        "/setroommates - Set the list of roommates\n"
        "/getroommates - Get the list of roommates",
        parse_mode=ParseMode.HTML,
    )

# Command: /currency
# this function is used to set the currency symbol and view the current currency symbol. it uses a global variable to store the currency symbol.
async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CURRENCY_SYMBOL
    args = context.args
    if not args:
        await update.message.reply_text(
            f"Current currency symbol is: {CURRENCY_SYMBOL}"
        )
        return
    CURRENCY_SYMBOL = args[0]
    await update.message.reply_text(
        f"Currency symbol set to: {CURRENCY_SYMBOL}"
    )

# Command: /setroom
# this function is used to set the room information and store it as a global variable. 
async def setroom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please enter the room details in the format:\n"
        "Hotel Name , Dates , Beds , Room Type"
    )
    return SET_ROOM_INFO  # Proceed to the next state

# this function receives the room information from the user and stores it as a global variable.
async def receive_room_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    room_details_text = update.message.text.strip()
    parts = [part.strip() for part in room_details_text.split(',')]
    if len(parts) != 4:
        await update.message.reply_text(
            "Please enter all the room details in the correct format."
        )
        return ConversationHandler.END
    room_info = {
        'Hotel Name': parts[0],
        'Dates': parts[1],
        'Beds': parts[2],
        'Room Type': parts[3]
    }
    context.chat_data['room_info'] = room_info
    await update.message.reply_text("Room information saved.")
    return ConversationHandler.END 

# Command: /getroom
# this function is used to get the room information from the global variable and send it back to the user. currently stored in local memory. TODO - use database.
async def getroom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    room_info = context.chat_data.get('room_info')
    if room_info:
        room_details_text = (
            "<pre>\n"
            f"<b>Hotel Name: </b>{room_info['Hotel Name']}\n"
            f"<b>Dates: </b>{room_info['Dates']}\n"
            f"<b>Beds: </b>{room_info['Beds']}\n"
            f"<b>Room Type: </b> {room_info['Room Type']}\n"
            "</pre>"
        )
        await update.message.reply_text(
            f"<b>Room Information:</b>\n{room_details_text}",
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text("No room information set.")

# Command: /setroommates
# this function is used to set the roommates for the user. currently stored in local memory. TODO - use database.
async def setroommates_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please enter the usernames or names of the roommates, separated by commas."
    )
    return SET_ROOMMATES  # Proceed to the next state

async def receive_roommates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    roommates_text = update.message.text.strip()
    roommates = [name.strip() for name in roommates_text.split(',')]
    context.chat_data['roommates'] = roommates
    await update.message.reply_text("Roommates list saved.")
    return ConversationHandler.END

# Command: /getroommates
# this function is used to get the roommates for the user. currently stored in local memory. TODO - use database.
async def getroommates_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    roommates = context.chat_data.get('roommates')
    if roommates:
        roommates_list = "\n".join(roommates)
        await update.message.reply_text(
            f"<b>Roommates:</b>\n{roommates_list}",
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text("No roommates set.")

# Command: /split
# this function is used to split the bill. currently stored in local memory. TODO - use database.
async def split_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "Usage: /split <total_cost> <number_of_roommates> [names...] [nights_stayed...]"
        )
        return

    try:
        total_cost = float(args[0])
        num_roommates = int(args[1])

        # Initialize variables
        names = []
        nights = []

        # Parse names and nights stayed
        remaining_args = args[2:]

        # Check if the next args are names (could be mentions or text)
        for arg in remaining_args:
            if arg.isdigit():
                break
            else:
                names.append(arg)

        # The rest are nights stayed
        nights_args = remaining_args[len(names):]
        nights = list(map(int, nights_args)) if nights_args else []

        # Use stored roommates if names are not provided
        if not names and 'roommates' in context.chat_data:
            names = context.chat_data['roommates']
            if len(names) != num_roommates:
                await update.message.reply_text(
                    "The number of stored roommates does not match the number provided."
                )
                return

        # Validate names and nights
        if names and len(names) != num_roommates:
            await update.message.reply_text(
                "The number of names provided does not match the number of roommates."
            )
            return

        if nights and len(nights) != num_roommates:
            await update.message.reply_text(
                "The number of nights stayed must match the number of roommates."
            )
            return

        # Begin building the message
        message_lines = []

        # Include room info if available
        room_info = context.chat_data.get('room_info')
        if room_info:
            room_details_text = (
                "<pre>\n"
                f"<b>Hotel Name: </b> {room_info['Hotel Name']}\n"
                f"<b>Dates: </b> {room_info['Dates']}\n"
                f"<b>Beds: </b> {room_info['Beds']}\n"
                f"<b>Room Type: </b> {room_info['Room Type']}\n"
                "</pre>"
            )
            message_lines.append("<b>Room Information:</b>")
            message_lines.append(room_details_text)

        if not nights:
            # Equal split
            share = total_cost / num_roommates
            share_formatted = f"{CURRENCY_SYMBOL}{share:.2f}"

            # Format the message
            if not names:
                names = [f"Person {i+1}" for i in range(num_roommates)]

            message_lines.extend([
                f"<b>Room Cost Split (Equal Share):</b>",
                f"Total Cost: {CURRENCY_SYMBOL}{total_cost:.2f}",
                f"Number of Roommates: {num_roommates}",
                ""
            ])

            for name in names:
                message_lines.append(f"{name}: <b>{share_formatted}</b>")
        else:
            total_nights = sum(nights)
            shares = [(n / total_nights) * total_cost for n in nights]

            # Format the message
            if not names:
                names = [f"Person {i+1}" for i in range(num_roommates)]

            message_lines.extend([
                f"<b>Room Cost Split (Based on Nights Stayed):</b>",
                f"Total Cost: {CURRENCY_SYMBOL}{total_cost:.2f}",
                f"Total Nights: {total_nights}",
                ""
            ])

            for i, (name, share, night) in enumerate(zip(names, shares, nights)):
                share_formatted = f"{CURRENCY_SYMBOL}{share:.2f}"
                message_lines.append(f"{name} ({night} nights): <b>{share_formatted}</b>")

        message = "\n".join(message_lines)

        # Add inline keyboard for acknowledgment
        acknowledge_button = InlineKeyboardButton(
            "Acknowledge", callback_data='acknowledge'
        )
        keyboard = InlineKeyboardMarkup([[acknowledge_button]])

        sent_message = await update.message.reply_text(
            message, parse_mode=ParseMode.HTML, reply_markup=keyboard
        )

        # Store message ID and initialize acknowledgment set
        context.chat_data['message_id'] = sent_message.message_id
        acknowledgments[sent_message.message_id] = set()

    except ValueError:
        await update.message.reply_text("Please enter valid numbers.")

# Callback handler for button presses
# this function is called when the button is pressed. It appends the user ID to the message
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    message_id = query.message.message_id

    if query.data == 'acknowledge':
        if user_id not in acknowledgments[message_id]:
            acknowledgments[message_id].add(user_id)
            # Update the message to show acknowledgments
            acknowledgers = []
            for uid in acknowledgments[message_id]:
                user = await context.bot.get_chat_member(
                    update.effective_chat.id, uid
                )
                username = user.user.username
                if username:
                    acknowledgers.append(f"@{username}")
                else:
                    acknowledgers.append(f"{user.user.first_name}")

            # Split the message at the acknowledgment section
            if "\n\n<b>Acknowledged by:</b>" in query.message.text:
                updated_text = query.message.text.split("\n\n<b>Acknowledged by:</b>")[0]
            else:
                updated_text = query.message.text

            updated_text += "\n\n<b>Acknowledged by:</b>\n" + "\n".join(acknowledgers)

            await query.edit_message_text(
                text=updated_text,
                parse_mode=ParseMode.HTML,
                reply_markup=query.message.reply_markup
            )
        else:
            await query.answer("You have already acknowledged this message.", show_alert=True)

# Command: /remind
#this command sends a "reminder" message. This will need to be updated to reference the room, and user ID associated with the room split.
async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Reminder: Please settle your room costs!"
    )

# main function, runs the builder for the telegram bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Conversation handlers
    room_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('setroom', setroom_command)],
        states={
            SET_ROOM_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_room_info)],
        },
        fallbacks=[],
    )

    roommates_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('setroommates', setroommates_command)],
        states={
            SET_ROOMMATES: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_roommates)],
        },
        fallbacks=[],
    )

    # Add handlers to the application
    app.add_handler(room_conv_handler)
    app.add_handler(roommates_conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("split", split_command))
    app.add_handler(CommandHandler("currency", currency_command))
    app.add_handler(CommandHandler("remind", remind_command))
    app.add_handler(CommandHandler("getroom", getroom_command))
    app.add_handler(CommandHandler("getroommates", getroommates_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-

import logging
import random
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

words = []

with open("words.txt") as f:
    for w in f:
        words.append(w.strip())

chats = {}

def word(bot, update):
    chat_id = update.message.chat_id

    if chat_id not in chats:
        chats[chat_id] = {"current": "", "correct": "", "solved": True}

    if chats[chat_id]["solved"]:
        new_w = list(random.choice(words))
        print("".join(new_w))
        chats[chat_id]["correct"] = "".join(new_w)

        random.shuffle(new_w)
        chats[chat_id]["current"] = "".join(new_w)

        chats[chat_id]["solved"] = False

    update.message.reply_text("The word to solve is: \n" + chats[chat_id]["current"])



def solve(bot, update):
    chat_id = update.message.chat_id

    if chat_id not in chats:
        chats[chat_id] = {"current": "", "correct": "", "solved": True}

    if chats[chat_id]["solved"] or chats[chat_id]["correct"] == "":
        update.message.reply_text("no active word, get a new one /word")
        return

    chats[chat_id]["solved"] = True
    update.message.reply_text("The correct word is: \n" + chats[chat_id]["correct"])

def check(bot, update):
    chat_id = update.message.chat_id
    user = update.message.from_user
    solution = update.message.text.strip()


    if chat_id not in chats:
        chats[chat_id] = {"current": "", "correct": "", "solved": True}

    solution = solution.lower()

    if not chats[chat_id]["solved"] and solution == chats[chat_id]["correct"]:
        update.message.reply_text(user["first_name"] + " solved the word 🥳🥳")
        chats[chat_id]["solved"] = True

def error(context):
    """Log Errors caused by Updates."""
    logger.warning('error "%s"', context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.environ["BOT_TOKEN"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("word", word))
    dp.add_handler(CommandHandler("solve", solve))

    dp.add_handler(MessageHandler(Filters.text, check))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
